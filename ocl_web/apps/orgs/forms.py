import floppyforms


class OrganizationCreateForm(floppyforms.Form):

    short_name = floppyforms.CharField(
        label="Organization Short Name",
        max_length="48",
        widget=floppyforms.TextInput(
            attrs={'id': 'orgShortName',
                   'placeholder': "Short Name (e.g. WHO)",
                   'class': 'form-control'}))

    full_name = floppyforms.CharField(
        label="Organization Full Name",
        max_length="48",
        widget=floppyforms.TextInput(
            attrs={'id': 'orgFullName',
                   'placeholder': "Full Name (e.g. World Health Organization)",
                   'class': 'form-control'}))

    website = floppyforms.URLField(
        label="Website",
        widget=floppyforms.URLInput(
            attrs={'id': 'orgWebsite',
                   'placeholder': "Website (e.g. http://www.who.int",
                   'class': 'form-control'}))


    @classmethod
    def submit(cls, data, *args, **kwargs):

        # utils.ocl_requests.post()
        # if not request.ok:
        # raise a Validation Error
        # else:
        # return True
        pass
