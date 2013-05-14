$ ->
    $("#id_unique").on 'click', () ->
        $("label[for=unique_relative], #id_unique_relative")[if this.checked then "hide" else "show"]()

    $.ajax
        url: "/admin/add_entry/start_pdbase" 
        data:
            entry_id: $('#entry_id').attr "value"
            format: 'json'
        success: (data) ->
            $("#virus_form").attr "hidden", not data.pdbase
            $(".message").attr "hidden", data.pdbase
        error: (err) ->
            console.log err
            # location.reload()
        dataType: 'json'

    $("#virus_form").submit (e) ->
        e.preventDefault()
        
        formErrors = []
        $(".control-group.error").removeClass "error"
        $(".required").each (index, field) ->
            if (!field.value?) or field.value is ""
                formErrors.push field

        $(formErrors).parents('.control-group').addClass "error"
        
        if _.isEmpty(formErrors)
            return e.currentTarget.submit()

        false