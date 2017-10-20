from django import forms

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class ComboBoxWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        self._name = name
        self._list = data_list
        self._css_class = kwargs.pop('css_class', '')
        super(ComboBoxWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        txt_name = "id_%s" % name
        btn_name = "btn_%s" % name
        cbo_name = "cbo_%s" % name
        list_text = ''
        list_count = 0
        for item in self._list:
            if (isinstance(item, list)):
                list_text += '["{1}","{0}"],'.format(item[0], item[1])
            else:
                list_text += '"{0}",'.format(item)
            list_count += 1

        text_html = super(ComboBoxWidget, self).render(name, value,
                                                       attrs={"class":"dropdown-input form-control {0}".format(self._css_class)})

        button_html = '<button id="{0}" class="dropdown-btn form-control {2}" type="button" onClick="Awesomplete.CBO_CLICK({1});">' \
                      '<span class="caret"></span></button>'.format(btn_name, cbo_name, self._css_class)

        script_html = '<script>' \
                      '   var {0} = document.getElementById("{0}"); ' \
                      '	  var {1} = new Awesomplete({0}, {{' \
                      '       minChars: 0, ' \
                      '       maxItems: {2}, ' \
                      '       list: [{3}] ' \
                      '   }}); ' \
                      '</script>'.format(txt_name, cbo_name, str(list_count), list_text)

        cbo_html = text_html + button_html + script_html

        return '<div>{0}</div>'.format(cbo_html)

class MultipleInputWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        self._name = name
        self._list = data_list
        self._css_class = kwargs.pop('css_class', '')
        super(MultipleInputWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        list_text = ''
        list_count = 0
        for item in self._list:
            if (isinstance(item, list)):
                list_text += '["{1}","{0}"],'.format(item[0], item[1])
            else:
                list_text += '"{0}",'.format(item)
            list_count += 1

        text_html = super(MultipleInputWidget, self).render(name, value,
                                                       attrs={'data-multiple':True, 'class':'form-control {0}'.format(self._css_class)})

        script_html = \
            '<script>' \
            'new Awesomplete("input[data-multiple]", {{' \
            '	filter: function(text, input) {{' \
            '		return Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);' \
            '	}},' \
            '	item: function(text, input) {{' \
            '		return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);' \
            '	}},' \
            '	replace: function(text) {{' \
            '		var before = this.input.value.match(/^.+,|/)[0];' \
            '       var code = text.match(/\[([a-z]+)\]/)[1];' \
            '       if (before.length > 0 && before.substr(-1) != ",") {{' \
            '           code = ", " + code;' \
            '       }}' \
            '		this.input.value = before + code;' \
            '	}},' \
            '   sort: Awesomplete.SORT_STANDARD, ' \
            '   minChars: 1,' \
            '   maxItems: {0}, ' \
            '   list: [{1}] ' \
            '}});' \
            '</script>'.format(str(list_count),list_text)

        return text_html + script_html
