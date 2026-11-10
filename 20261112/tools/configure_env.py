"""선택한 난이도의 실습 .env를 준비합니다. 비밀번호는 화면에 표시하지 않습니다."""
from pathlib import Path
from getpass import getpass
import argparse
import shutil
from sqlalchemy import URL
from dotenv import set_key

LEVELS = {'1': ('01_기본필수', 'basic'), '2': ('02_응용', 'applied'),
          '3': ('03_심화', 'advanced'), '4': ('04_특심화', 'expert')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level', choices=LEVELS, required=True, help='1 기본필수 / 2 응용 / 3 심화 / 4 특심화')
    parser.add_argument('--exercise', default='all', choices=['all'] + [str(x) for x in range(1, 9)])
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5432)
    parser.add_argument('--user', default='day19_user')
    parser.add_argument('--overwrite', action='store_true', help='기존 .env의 연결값을 명시적으로 갱신')
    args = parser.parse_args()
    role_root = Path(__file__).resolve().parents[1]
    directory, tag = LEVELS[args.level]
    candidates = sorted((role_root / directory).glob('실습[0-9][0-9]_*'))
    if args.exercise != 'all':
        candidates = [p for p in candidates if p.name.startswith(f'실습{int(args.exercise):02d}_')]
    targets = [p for p in candidates if args.overwrite or not (p / '.env').exists()]
    if not targets:
        print('작성할 .env가 없습니다. 기존 값은 유지했습니다.')
        return
    password = getpass('수업 DB 계정 비밀번호(입력해도 보이지 않음): ')
    if not password:
        raise SystemExit('빈 비밀번호는 저장하지 않습니다.')
    for exercise in targets:
        number = int(exercise.name[2:4])
        path = exercise / '.env'
        if not path.exists():
            shutil.copyfile(exercise / '.env.example', path)
        # URL.create가 @, :, /, # 등의 비밀번호 문자를 올바르게 인코딩합니다.
        url = URL.create('postgresql+psycopg', username=args.user, password=password,
                         host=args.host, port=args.port, database=f'day19_{tag}_{number:02d}')
        set_key(str(path), 'DATABASE_URL', url.render_as_string(hide_password=False), quote_mode='always')
        set_key(str(path), 'TEST_DATABASE_URL',
                url.set(database=f'day19_{tag}_{number:02d}_test').render_as_string(hide_password=False),
                quote_mode='always')
        print(f'준비 완료: {directory}/{exercise.name}/.env')
    print('.env는 제출하거나 Git에 올리지 마세요. 접속값은 출력하지 않았습니다.')


if __name__ == '__main__':
    main()
