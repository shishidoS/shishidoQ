from django import forms

class InputForm(forms.Form):
    company = forms.ChoiceField(
        choices=[('company1', '会社1'), ('company2', '会社2'), ('company3', '会社3')],
        label='会社名を選択してください'
    )
    store = forms.ChoiceField(
        choices=[('store1', '店舗1'), ('store2', '店舗2'), ('store3', '店舗3')],
        label='店舗名を選択してください'
    )
    staff = forms.ChoiceField(
        choices=[('staff1', 'スタッフ1'), ('staff2', 'スタッフ2'), ('staff3', 'スタッフ3')],
        label='担当スタッフを選択してください'
    )
    subject = forms.CharField(
        label='題名を入力してください',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '題名を入力'})
    )
    message = forms.CharField(
        label='問い合わせ内容を入力してください',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': '問い合わせ内容を入力'})
    )

