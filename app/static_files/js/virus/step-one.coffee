$ ->
    $("#initial_virus_form").submit (e)->
        e.preventDefault()

        error = false
        $(".control-group.error").removeClass "error"
        $(".required").each (index, field) ->
            if (!field.value?) or field.value is ""
                $(field).parents('.control-group').addClass "error"
                error = true
        if (error)
            return not error

        $.ajax
            url: "http://localhost:8000/api/v1/virus"
            data: 
                entry_id: $("#id_entry_id").val()
                format: 'json' 
            dataType: 'json'
            success: (data) ->
                confirm_delete = true
                if data.objects.length > 0 
                    confirm_delete = confirm "Virus exists already, continuing will delete the existing entry!"
                    e.currentTarget.submit() if confirm_delete
                else
                    e.currentTarget.submit()
            error: ->
                alert 'omg'

        false