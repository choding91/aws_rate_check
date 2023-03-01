from rest_framework.views import APIView
from django.http import HttpResponse
import requests, zipfile, io, os, shutil
import pandas as pd


class UsageView(APIView):
    def get(self, request):
        url = "http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip"

        try:
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
        except:
            return HttpResponse("URL 경로에 파일이 없습니다.")

        url_zip = url.replace(".zip", "")
        url_filename = url_zip.split("/")[-1]

        csv = pd.read_csv(
            url_filename,
            encoding="utf-8",
        )

        os.remove(url_filename)
        shutil.rmtree("__MACOSX")

        start = csv["TimeInterval"].str[:20]
        csv["datetime"] = pd.to_datetime(start)
        csv["year"] = csv["datetime"].dt.year
        csv["month"] = csv["datetime"].dt.month

        year = 2022
        month = 11

        try:
            find_column = csv.loc[(csv["year"] == year) & (csv["month"] == month)]
        except:
            return HttpResponse("올바른 year, month를 입력해 주세요.")

        path = os.path.join(os.path.expanduser("~"), "Desktop", "usage.csv")
        find_column.to_csv(path)
        os.popen(path)

        return HttpResponse(f"바탕화면에 필터된 CSV 파일 저장 완료하였습니다. (저장 경로 - {path})")


class BillView(APIView):
    def post(self, request):
        url = "http://dtgqz5l2d6wuw.cloudfront.net/coding_test_1.csv.zip"

        try:
            r = requests.get(url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall()
        except:
            return HttpResponse("URL 경로에 파일이 없습니다.")

        url_zip = url.replace(".zip", "")
        url_filename = url_zip.split("/")[-1]

        csv = pd.read_csv(
            url_filename,
            encoding="utf-8",
        )

        os.remove(url_filename)
        shutil.rmtree("__MACOSX")

        start = csv["TimeInterval"].str[:20]
        csv["datetime"] = pd.to_datetime(start)
        csv["year"] = csv["datetime"].dt.year
        csv["month"] = csv["datetime"].dt.month

        userId = request.POST["id"]
        year = request.POST["year"]
        month = request.POST["month"]

        try:
            find_column = csv.loc[(csv["userId"] == int(userId)) & (csv["year"] == int(year)) & (csv["month"] == int(month))]
        except:
            return HttpResponse("올바른 id, year, month를 입력해 주세요.")

        cost_krw = find_column["exchangeRate"].mul(find_column["Cost"])
        find_column["cost_krw"] = cost_krw.sum()
        find_column["cost"] = find_column["Cost"].sum()
        find_column["exchange_rate"] = find_column["exchangeRate"].mean()

        check = find_column[["exchange_rate", "cost", "cost_krw"]]
        result = check.iloc[0]

        path = os.path.join(os.path.expanduser("~"), "Desktop", "bill.json")
        result.to_json(path)
        os.popen(path)

        return HttpResponse(f"바탕화면에 필터된 JSON 파일 저장 완료하였습니다. (저장 경로 - {path})")
