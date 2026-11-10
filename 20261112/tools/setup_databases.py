"""강사와 함께 실행하는 PostgreSQL 준비 도구. 새 DB만 만들고 기존 데이터는 바꾸지 않습니다."""
from getpass import getpass
import argparse
import psycopg
from psycopg import sql

TAGS = {'1': 'basic', '2': 'applied', '3': 'advanced', '4': 'expert'}


def provision(connection, app_user, level, exercises, new_password=None):
    """새 역할/DB만 생성합니다. 기존 역할의 비밀번호나 DB 소유권은 바꾸지 않습니다."""
    if not connection.autocommit:
        raise ValueError('CREATE DATABASE는 autocommit 관리 연결에서 실행해야 합니다.')
    exists = connection.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (app_user,)).fetchone()
    if not exists:
        if not new_password:
            raise ValueError('새 계정 비밀번호가 필요합니다.')
        connection.execute(sql.SQL('CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD {}').format(
            sql.Identifier(app_user), sql.Literal(new_password)))
        print(f'새 수업 계정 생성: {app_user}')
    else:
        print(f'기존 수업 계정 유지: {app_user}')
    for number in exercises:
        for suffix in ('', '_test'):
            database = f'day19_{TAGS[level]}_{number:02d}{suffix}'
            owner = connection.execute('SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname=%s',
                                       (database,)).fetchone()
            if owner:
                print(f'기존 DB 유지: {database} (소유자: {owner[0]})')
                if owner[0] != app_user:
                    print('  소유자가 다릅니다. 강사와 해당 DB의 권한을 확인하세요.')
                continue
            connection.execute(sql.SQL('CREATE DATABASE {} OWNER {}').format(
                sql.Identifier(database), sql.Identifier(app_user)))
            print(f'새 DB 생성: {database}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level', required=True, choices=TAGS)
    parser.add_argument('--exercise', default='all', choices=['all'] + [str(x) for x in range(1, 9)])
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5432)
    parser.add_argument('--admin-user', default='postgres')
    parser.add_argument('--app-user', default='day19_user')
    args = parser.parse_args()
    password = getpass('PostgreSQL 관리자 계정 비밀번호(입력해도 보이지 않음): ')
    numbers = list(range(1, 9)) if args.exercise == 'all' else [int(args.exercise)]
    try:
        with psycopg.connect(host=args.host, port=args.port, user=args.admin_user,
                             password=password, dbname='postgres', connect_timeout=5, autocommit=True) as connection:
            exists = connection.execute('SELECT 1 FROM pg_roles WHERE rolname=%s', (args.app_user,)).fetchone()
            new_password = None
            if not exists:
                new_password = getpass('새 수업 계정 비밀번호: ')
                if not new_password or new_password != getpass('새 수업 계정 비밀번호 다시 입력: '):
                    raise SystemExit('비밀번호가 비어 있거나 서로 다릅니다. 변경하지 않았습니다.')
            provision(connection, args.app_user, args.level, numbers, new_password)
    except psycopg.Error as error:
        raise SystemExit(f'DB 준비 실패: {type(error).__name__}. Host·Port·관리 계정·권한을 강사와 확인하세요.') from None
    print('준비 완료. 앱의 .env에는 관리자 대신 수업 계정을 사용하세요.')


if __name__ == '__main__':
    main()
