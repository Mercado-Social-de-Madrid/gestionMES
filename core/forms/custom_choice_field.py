from django import forms


class ChoiceFieldWithTitles(forms.ChoiceField):

    def __init__(self, choices=(), *args, **kwargs):
        choice_pairs = [(c[0], c[1]) for c in choices]
        super(ChoiceFieldWithTitles, self).__init__(choices=choice_pairs, *args, **kwargs)
        self.widget.titles = dict([(c[1], c[2]) for c in choices])