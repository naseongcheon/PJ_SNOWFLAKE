# -*- coding: utf-8 -*-

import cx_Oracle
import boto3
import csv
import os


# 오라클 접속 class
class OracleConnection:
    # 접속 정보 초기화
    def __init__(self, host, port, sid, user, passwd) -> None:
        self.connection = None
        self.cursor = None
        self.user = user
        self.passwd = passwd
        
        # 오라클 주소 정보
        self.tns = cx_Oracle.makedsn(host, port, sid)
        
        # 오라클 인스턴트 클라이언트 위치 설정
        cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_9")

    # 특정 유저로 오라클에 접속 
    def connect(self):
        try:
            # 오라클 접속 유저 정보
            self.connection = cx_Oracle.connect(self.user, self.passwd, self.tns)
        except cx_Oracle.DatabaseError as e:
            print("Could not connect to Oracle: ", e)

        # 데이터 담을 메모리의 이름
        self.cursor = self.connection.cursor()

    def close(self):
            self.cursor.close()
            self.connection.close()


# S3 접속 class
class S3Connection():
    # AWS 계정 정보 초기화
    def __init__(self, service, region, access_id, access_key) -> None:
        self.service_name = service
        self.region_name = region
        self.access_id = access_id
        self.access_key = access_key

    # AWS 클라이언트 연결
    def connect(self):
        self.client = boto3.client(
            service_name=self.service_name,
            region_name=self.region_name,
            aws_access_key_id=self.access_id,
            aws_secret_access_key=self.access_key
        )
    

# 오라클 유저 정보 입력
oralce_conn = OracleConnection("10.90.3.166", 1521, "xe", "c##mason", "mason")

# 오라클 클라이언트에 접속
oralce_conn.connect()

try:
    # 쿼리 결과가 cursor 메모리에 저장됨
    oralce_conn.cursor.execute("SELECT * FROM T_SUBWAY_TIME_GETON_M")
    
    # 메모리에 담긴 데이터를 한 행씩 전부 fetch
    rows = oralce_conn.cursor.fetchall()
    
    # 승차 정보 파일 생성(이어쓰기 모드: a)
    f = open("D:\\데이터솔루션팀\\PROJECT\\subway_time_geton_m.csv", "a", newline="")
    wr = csv.writer(f)
    for row in rows:
        wr.writerow(list(row))
    f.close()
    
    # 하차 정보 테이블의 데이터 모두 호출
    oralce_conn.cursor.execute("SELECT * FROM T_SUBWAY_TIME_GETOFF_M")
    rows = oralce_conn.cursor.fetchall()

    # 하차 정보 파일 생성
    f = open("D:\\데이터솔루션팀\\PROJECT\\subway_time_getoff_m.csv", "a", newline="")
    wr = csv.writer(f)
    for row in rows:
        wr.writerow(list(row))
    f.close()

# 예외 처리
except Exception as e:
    print("Could not execute the query", e)

finally:
    oralce_conn.close()




# S3 계정 정보 입력
s3_conn = S3Connection("s3","ap-northeast-2","AKIAXSMRRG6TPELTPAC7","vJDqyEbkxila7BzX7sDtAhr9Y76AAG65NWLg2Upd")
s3_conn.connect()

# S3에 생성된 버킷 목록
# print(s3_conn.client.list_buckets())

# 특정 버킷의 오브젝트 목록
# print(s3_conn.client.list_objects(Bucket='datasolution-subway'))


# 버킷에 파일 업로드(로컬 파일명, 버킷명, 키)
s3_conn.client.upload_file(
    'D:\\데이터솔루션팀\\PROJECT\\subway_time_geton_m.csv', # 승차 정보
    'datasolution-subway',
    'seoul/subway_time_geton.csv',
    ExtraArgs={'ACL':'public-read'}
)

s3_conn.client.upload_file(
    'D:\\데이터솔루션팀\\PROJECT\\subway_time_getoff_m.csv', # 하차 정보
    'datasolution-subway',
    'seoul/subway_time_getoff.csv',
    ExtraArgs={'ACL':'public-read'}
)