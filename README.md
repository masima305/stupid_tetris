# 조금 다른 테트리스

## 기본 테트리스 소스에서, 블럭을 조금 변형시키고 사운드를 삽입한 소스입니다.

기본 적인 소스는 다음의 코드에서 clone해온것임을 밝힙니다.
https://gist.github.com/ryukinix/87a222017b377322f8fafa3943ceff55


----
## 시작화면

### 아무키나 누르면 게임이 시작됩니다.

![start](https://github.com/masima305/stupid_tetris/blob/master/start.png)
----

### 게임이 진행되는 과정에서 'p'버튼을 누르면 정지시킬 수 있습니다.
![pause](https://github.com/masima305/stupid_tetris/blob/master/Pause.png)

----


----
### 가장 중요한 부분은 블럭으로, 기존의 블럭 보모양이 아닌
### 조금 더 난이도 있는 블럭 모양이 내려옵니다.

### 종류는 다음과 같습니다.
![blocks](https://github.com/masima305/stupid_tetris/blob/master/blocks.png)
----


### 총 6가지로, 화면에 더이상 블럭을 놓을 자리가 없으면 그대로 게임오버됩니다.
![over](https://github.com/masima305/stupid_tetris/blob/master/GameOver.png)

---

# 기능

1. 키 조작
	1.1 오른쪽 방향키 / d => 블럭이 오른쪽으로 이동
	1.2 왼쪽 방향키 / a => 블럭이 왼쪽으로 이동
	1.3 윗쪽 방향키 / q / w => 블럭 회전
	1.4 아랫쪽 방향키 / s => 블럭 서서히 떨어뜨리기
	1.5 스페이스바 => 블럭 한번에 떨어뜨리기
	1.6 p => 게임 일시 중단

2. 점수
	* 한줄이 완성되면 그 줄은 사라지고 점수가 1점 증가합니다. 10점당 level이 하나씩 올라갑니다.

3. 추가적 구현목록
	3.1 플레이를 하는동안 배경 음악이 나옵니다.
	3.2 게임 오버되면 총소리가 나오면서 게임이 끝납니다.
	3.3 처음 게임을 시작하기 전 메인 화면이 더 이쁘게 나옵니다.
	3.4 블럭이 기본적으로 제공되는것보다 더 다양하게 나옵니다.
	3.5 게임 화면이 더 커졌습니다.
