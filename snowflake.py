import snowflake.connector


            
        
# Snowflake Connector 인스턴스 생성
sf_cnx = snowflake.connector.connect(
    user='datasolution',
    password='P@ssw0rd',
    account='fr94818.ap-northeast-2.aws'
)



try:
    sf_cnx.cursor().execute("USE DATABASE project")
    sf_cnx.cursor().execute("USE SCHEMA subway")
    
    # CSV 파일 로드
    sf_cnx.cursor().execute("COPY INTO T_SUBWAY_TIME_GETON_M FROM 's3://datasolution-subway/seoul/subway_time_geton.csv' file_format = (format_name = CSV_FILEFORMAT ) ")
# 예외 처리
except Exception as e:
    print("Could not execute the query", e)

finally:
    sf_cnx.close()





# 테이블 생성
# sf_cnx.cursor().execute("CREATE OR REPLACE TABLE T_SUBWAY_TIME_GETON_M " + 
#                         " (	"SEQ" INTEGER  NOT NULL , " + 
#                         "        "SUBWAY_MONTH" VARCHAR2(6), " + 
#                         "        "SUBWAY_LINE" VARCHAR2(50),  " +
#                         "        "SUBWAY_NAME" VARCHAR2(50), " +
#                         "        "TIME4_5" INTEGER, " +
#                         "        "TIME5_6" INTEGER, " +
#                         "        "TIME6_7" INTEGER, " +
#                         "        "TIME7_8" INTEGER, " +
#                         "        "TIME8_9" INTEGER, " +
#                         "        "TIME9_10" INTEGER, " +
#                         "        "TIME10_11" INTEGER, " +
#                         "        "TIME11_12" INTEGER, " +
#                         "        "TIME12_13" INTEGER, " +
#                         "        "TIME13_14" INTEGER, " +
#                         "        "TIME14_15" INTEGER, " +
#                         "        "TIME15_16" INTEGER, " +
#                         "        "TIME16_17" INTEGER, " +
#                         "        "TIME17_18" INTEGER," +
#                         "        "TIME18_19" INTEGER, " +
#                         "        "TIME19_20" INTEGER, " +
#                         "        "TIME20_21" INTEGER, " +
#                         "        "TIME21_22" INTEGER, " +
#                         "        "TIME22_23" INTEGER, " +
#                         "        "TIME23_24" INTEGER, " +
#                         "        "TIME00_01" INTEGER, " +
#                         "        "TIME01_02" INTEGER, " +
#                         "        "TIME02_03" INTEGER, " +
#                         "        "TIME03_04" INTEGER," +
#                         "        CONSTRAINT PK_SUBWAY_TIME_GETON_M PRIMARY KEY (SEQ) " +
#                         "    );")

