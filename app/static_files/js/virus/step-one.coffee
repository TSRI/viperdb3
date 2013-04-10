$ ->
    $("#virus_form_submit").on 'click', (e)->
        e.currentTarget.attr 'disabled', true

        promise = $.ajax
            url: "http://localhost:8000/api/v1/virus"
            data: 
                entry_id: $("#id_entry_id").val()
                format: 'json' 
            dataType: 'json'

        promise.done (data) ->
            confirm_delete = true
            if data.objects.length > 0 
                confirm_delete = confirm "Virus exists already, continuing will delete the existing entry!"
                delete_existing_entry data.objects[0].entry_id if confirm
        promise.fail ->
            alert 'omg'
            
        false

    delete_existing_entry = (entry_id) ->
        promise = $.ajax
            url: "/admin/add_entry/delete_entry"
            data:
                entry_id: entry_id
        promise.done = ->