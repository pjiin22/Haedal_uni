# probability.py

"""
ProbabilityManager 클래스는 시간 경과와 신뢰도를 기반으로
빈 강의실일 확률(%)을 계산하는 기능을 제공합니다.
"""

class ProbabilityManager:
    def __init__(self, max_duration_min=180):
        """
        생성자: 최대 사용 시간 설정 (기본 180분)
        """
        self.max_duration_min = max_duration_min

    def get_empty_probability(self, elapsed_time_min: int, trust_score: float) -> int:
        """
        빈 강의실 확률(%)을 계산합니다.
        
        Parameters:
        - elapsed_time_min: 경과된 시간 (분 단위)
        - trust_score: 사용자의 신뢰도 (0~1)
        
        Returns:
        - 정수형 확률값 (0~100)
        """
        # 신뢰도 보정 (0~1 사이로)
        trust_score = max(0.0, min(trust_score, 1.0))

        # 경과 시간 비율 계산 (최대값 제한)
        elapsed_ratio = min(elapsed_time_min / self.max_duration_min, 1.0)

        # 신뢰도가 높을수록 확률 상승은 느려짐
        decay_speed = 1.0 - trust_score

        # 확률 계산 후 퍼센트로 변환
        probability = elapsed_ratio * decay_speed * 100

        return round(probability)