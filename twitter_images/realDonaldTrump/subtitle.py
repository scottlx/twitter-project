import srt
from datetime import timedelta
list =[1,2,3,4,5]
subs = []
for num in list:
	subs.append(srt.Subtitle(index=num, start=timedelta(seconds=num), end=timedelta(seconds=num+1), content='x'))
print(srt.compose(subs))