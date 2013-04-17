$ ->
    $("#virus_form").on 'submit', (e)->
        e.preventDefault()
        $("#virus_form_submit").attr 'disabled', true

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
                    delete_existing_entry data.objects[0].entry_id if confirm
                else
                    e.currentTarget.submit()
            error: ->
                alert 'omg'

        false

    delete_existing_entry = (entry_id) ->
        $.ajax(
            url: "/admin/add_entry/delete_entry"
            data:
                entry_id: entry_id
        ).done ->
            $("#virus_form").submit()
