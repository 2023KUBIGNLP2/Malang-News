import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import time
from tqdm import tqdm
import os


def save_csv(news_infos, check_start, check_end, save_path):
    print(f"---------------save {check_start} {check_end}---------------")
    print(f"---------------news_infos len {len(news_infos)}---------------")
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    df = pd.DataFrame(news_infos, columns=["title", "url"])
    df.to_csv(
        os.path.join(save_path, f"news_info_{check_start}_{check_end}.csv"), index=False
    )
    return list()


def crawler(delay, save_every, section, start_iter, end_iter, save_path):
    news_infos = []  # title, link
    check_start = start_iter
    # 2023년 8월 25일 기준 IT
    base_url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={section}#&date=%2000:00:00&page="
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    for i in tqdm(range(start_iter, end_iter + 1)):
        req = requests.get(f"{base_url}{i}", headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")  # html 문서 파싱
        newses = soup.findAll(
            "a", "sh_text_headline nclicks(cls_sci.clsart)"
        )  # 헤드라인 뉴스 제목의 태그와 class 속성 값
        for i, news in enumerate(newses):
            news_info = []
            news_info.append(news.text)
            news_info.append(news["href"])
            news_infos.append(news_info)

        if (i * len(newses)) % save_every == 0:
            news_infos = save_csv(news_infos, check_start, (i * len(newses)), save_path)
            check_start = i * len(newses)

        if delay:
            time.sleep(delay)

    save_csv(news_infos, check_start, (i * len(newses)), save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--delay", default=0, type=int, help="Crawling delay를 설정해 block을 방지합니다."
    )
    parser.add_argument(
        "-s", "--save_every", default=10000, type=int, help="저장되는 주기를 설정합니다."
    )
    parser.add_argument(
        "--section", default=105, type=int, help="네이버 뉴스 분야별 코드를 입력합니다. sid1=xxx"
    )
    parser.add_argument(
        "--start_iter", default=1, type=int, help="Crawling 시작 페이지를 지정합니다."
    )
    parser.add_argument(
        "--end_iter", default=10000, type=int, help="Crawling 종료 페이지를 지정합니다."
    )
    parser.add_argument(
        "--save_path", default="../data/user_info", type=str, help="저장할 경로를 지정합니다."
    )
    args = parser.parse_args()
    crawler(
        args.delay,
        args.save_every,
        args.section,
        args.start_iter,
        args.end_iter,
        args.save_path,
    )
