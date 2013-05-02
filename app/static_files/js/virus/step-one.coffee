$ ->
    $("#virus_form").on 'submit', (e)->
        e.preventDefault()
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