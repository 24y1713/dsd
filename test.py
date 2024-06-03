import streamlit as st
import random

def generate_fake_result():
    teams = ["Team A", "Team B", "Team C"]
    return random.choice(teams)

def calculate_payout(bet_amount, selected_team, result):
    if selected_team == result:
        payout = bet_amount * 2
    else:
        payout = 0
    commission = bet_amount * 0.1  # 베팅 금액의 10%를 수수료로 설정
    payout -= commission
    return payout, commission

def main():
    st.title("MSI 경기 결과 베팅")

    # 로그인
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    login_button = st.button("로그인")

    if login_button:
        # 간단한 인증을 위해 사용자 이름이 "admin"이고 비밀번호가 "password"인 경우에만 로그인 성공으로 가정합니다.
        if username == "admin" and password == "password":
            st.success("로그인 성공")
            st.session_state.logged_in = True
        else:
            st.error("잘못된 사용자 이름 또는 비밀번호")
            st.session_state.logged_in = False

    # 로그인 상태를 확인하여 게임을 진행합니다.
    if st.session_state.get("logged_in"):
        # 초기 소지금 설정
        initial_balance = round(random.uniform(50000, 150000))
        if "balance" not in st.session_state:
            st.session_state.balance = initial_balance
        
        st.write(f"현재 소지금: {st.session_state.balance}")

        # 베팅할 비율 선택
        bet_ratio = st.radio("베팅할 소지금의 비율 (%)", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

        # 소지금과 베팅 금액 계산
        balance_int = int(st.session_state.balance)
        bet_amount = int(balance_int * bet_ratio / 100)

        # 팀 선택
        selected_team = st.selectbox("베팅할 팀 선택", ["Team A", "Team B", "Team C"])
        
        # 베팅 버튼
        if st.button("베팅하기"):
            if balance_int < 0:
                st.error("소지금이 음수가 되어 게임을 종료합니다.")
            elif bet_amount > balance_int:
                st.error("소지금이 부족합니다.")
            else:
                # 결과 생성
                result = generate_fake_result()
                
                # 배당 계산
                payout, commission = calculate_payout(bet_amount, selected_team, result)
                
                # 결과 출력
                st.write(f"결과: {result}")
                st.write(f"배당금: {payout if payout > 0 else 0}")  # 배당금이 0보다 크면 그대로, 아니면 0으로 표시
                st.write(f"수수료: {commission}")
                
                # 소지금 업데이트
                st.session_state.balance = balance_int - bet_amount + payout
                st.write(f"남은 소지금: {st.session_state.balance}")

if __name__ == "__main__":
    main()
