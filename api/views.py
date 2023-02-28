from rest_framework.views import APIView
from django.http import HttpResponse
import requests, zipfile, io, os
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

        start = csv["TimeInterval"].str[:20]
        csv["datetime"] = pd.to_datetime(start, format="%Y-%m-%dT%H:%M:%SZ")
        csv["year"] = csv["datetime"].dt.year
        csv["month"] = csv["datetime"].dt.month

        year = 2022
        month = 11

        path = os.path.join(os.path.expanduser("~"), "Desktop", "usage.csv")

        try:
            if year & month != "":
                find_column = csv.loc[(csv["year"] == year) & (csv["month"] == month)]
                return HttpResponse(
                    "바탕화면에 필터된 CSV 파일 저장 완료되었습니다.", find_column.to_csv(path)
                )
        except:
            return HttpResponse("올바른 year, month를 입력해 주세요.")
