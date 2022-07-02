# 用于保存音频
import wave
#数学库
import numpy as np
import matplotlib.pyplot as plt

#中文支持和布局调整 
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['figure.figsize']=(15,8)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=0.5, hspace=0.5) #调整布局

def saveAudio(filename,data,params): #
    with wave.open(filename + '.wav', 'wb') as wavfile:
        print(params)
        wavfile.setparams(params)
        wavfile.writeframes(bytes(data))

def wavread(path): #传路径，利用wav组件读音频 调用getparams 一次性返回所有wav信息 返回元组-声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型
    wavfile = wave.open(path, "rb")
    params = wavfile.getparams()
    print(params)

    framesra, frameswav = params[2], params[3] #取得采样频率和采样点数
    datawav = wavfile.readframes(frameswav) #采样点数 越细腻返回帧数越多
    wavfile.close() 
    datause = np.frombuffer(datawav, dtype=np.short) #构建np的动态数组 返出去给画图要用
    datause.shape = -1, 2 #构建numpy数组实现转化为了画图
    datause = datause.T 
    time = np.arange(0, frameswav) * (1.0 / framesra)
    return datause, time, params

path = r"luvu.wav"
wavdata, wavtime, params = wavread(path) 

noise=np.random.rand(len(wavdata[0]))

noise_music = wavdata.copy() + noise #加上噪声 噪声随机 用wavdata做参数保证是声音
saveAudio("add_luvu", noise_music, params) 

transformed=np.fft.fft2(noise_music)  #傅立叶变换

avg1 = np.max(abs(transformed[0][1:]))/10000 #做变换
avg2 = np.max(abs(transformed[1][1:]))/10000
transformed[0][np.where(abs(transformed[0])<=avg1)]=0+0j
transformed[1][np.where(abs(transformed[1])<=avg2)]=0+0j

noise_music = np.fft.ifft2(transformed).astype(int) #astype(int)很重要，过滤掉浮点过小信号

plt.subplot(221) #画图 把原始图像分割（数字）
plt.title("original_wave")
plt.plot(wavdata[0][4000:4500])

plt.subplot(222)
plt.title("original_spectrogram")
plt.plot(np.fft.fft(wavdata[0][4000:4200]))

plt.subplot(223)
plt.title("processed_wave")
plt.plot(noise_music[0][4000:4500])

plt.subplot(224)
plt.title("processed_spectrogram")
plt.plot(np.fft.fft(noise_music[0][4000:4200]))

plt.show()
saveAudio("reversed_luvu", noise_music, params)















































































