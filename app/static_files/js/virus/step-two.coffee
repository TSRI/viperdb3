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
        dataType: 'json'

    $("#virus_form").submit (e) ->
        e.preventDefault()
        error = false
        $(".required").each (index, field) ->
            if (!field.value?) or field.value is ""
                $(field).parent().parent().addClass "error"
                error = true
        unless error
            e.currentTarget.submit()        
        not error