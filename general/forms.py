import json

from django import forms
from general.models import Mobile, VIDEO_CODEC_CHOICE, AUDIO_CODEC_CHOICE, AUDIO_SOURCE_CHOICE, RECORDER_FORMAT, \
    DEFAULT_SCRCPY_KWARGS


class MobileForm(forms.ModelForm):
    recorder_enable = forms.BooleanField(label="开启录屏", help_text="需要linux部署方式，window部署不可录屏", required=False)
    audio = forms.BooleanField(label="开启声音", help_text="需要安卓版本>=11，安卓版本=11需要提前解锁手机", required=False)
    control = forms.BooleanField(label="开启控制", help_text="可远程控制手机，控制关闭时仅可投屏", required=False)
    recorder_format = forms.ChoiceField(label="录屏格式", choices=RECORDER_FORMAT, required=False)
    video_codec = forms.ChoiceField(label='视频codec', choices=VIDEO_CODEC_CHOICE, required=False)
    video_codec_options = forms.CharField(label='视频codec参数', help_text="若无画面请尝试设置: profile=1,level=2", required=False)
    video_encoder = forms.CharField(label='视频codec_encoder', required=False, help_text="若无画面请尝试以下某一或者手机支持的其他encoder：OMX.google.h264.encoder | OMX.qcom.video.encoder.hevc | c2.android.hevc.encoder | c2.mtk.hevc.encoder")
    video_bit_rate = forms.IntegerField(label='视频比特率', help_text='800000, 此时视频比特率为800kbs', required=False)
    max_fps = forms.IntegerField(label='视频帧率', help_text='设置视频最大帧率', required=False)
    audio_codec = forms.ChoiceField(label='音频codec', choices=AUDIO_CODEC_CHOICE, required=False)
    audio_source = forms.ChoiceField(label='音频来源', choices=AUDIO_SOURCE_CHOICE,required=False)
    audio_codec_options = forms.CharField(label='音频codec参数', required=False)
    audio_encoder = forms.CharField(label='音频codec_encoder', required=False, help_text="若无音频请尝试以下某一或者手机支持的其他encoder：OMX.google.aac.encoder | c2.android.opus.encoder | c2.android.aac.encoder")
    audio_bit_rate = forms.IntegerField(label='音频比特率', help_text='128000, 此时音频比特率为128kbs', required=False)
    max_size = forms.IntegerField(label='最大尺寸', help_text='720, 此时输出视频最大尺寸为720', required=False)
    crop = forms.CharField(label='裁剪尺寸', help_text="1224:1440:0:0，以(0,0)为原点的1224x1440屏幕区域", required=False)
    show_touches = forms.BooleanField(label="显示点击", help_text="显示屏幕点击操作", required=False)
    stay_awake = forms.BooleanField(label="保持唤醒", help_text="连接时间内，屏幕保持常亮", required=False)
    power_off_on_close = forms.BooleanField(label='结束熄屏', required=False, help_text='结束连接时，屏幕熄灭')
    power_on = forms.BooleanField(label='开始亮屏', required=False, help_text='开始连接时，屏幕亮起')

    def get_initial_for_field(self, field, field_name):
        """
        Return initial data for field on form. Use initial data from the form
        or the field, in that order. Evaluate callable values.
        """
        value = self.initial.get(field_name, field.initial)
        if callable(value):
            value = value()
        return json.loads(self.instance.config).get(field_name, value)

    def clean(self):
        self._validate_unique = True
        config_dict = json.loads(self.instance.config)
        # update config_dict by form fields
        config_dict.update({field: self.cleaned_data[field] for field in self.cleaned_data if field in DEFAULT_SCRCPY_KWARGS})
        # valid mp4 video recorder
        if (config_dict['recorder_enable']) and (config_dict['recorder_format'] == 'mp4') and (config_dict['audio_codec'] != 'aac'):
            raise forms.ValidationError("recording: mp4 audio_codec only support aac!!!")
        # restore config_dict to config str
        self.cleaned_data['config'] = json.dumps(config_dict)
        return self.cleaned_data

    class Meta:
        model = Mobile
        fields = '__all__'
