from scipy import stats

x1=[0.9886,0.9922,0.995, 0.995, 0.995, 0.995, 0.995, 0.9942,0.9942]
x2=[0.9176,0.9569,0.95,0.9623,0.9587,0.958, 0.9601,0.9558,0.9542]

w,p = stats.ttest_rel(x1, x2)
print(w,p)
