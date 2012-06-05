$ ->
    $("#virus_form_submit").on 'click', ()->
        $.ajax
            url: "http://localhost:8000/api/v1/virus"
            data: 
                entry_id: $("#id_entry_id").val()
                format: 'json' 
            success: (data) ->
                confirm_delete = true
                if data.objects.length > 0 
                    confirm_delete = confirm "Virus exists already, continuing will delete the existing entry!"
                $("#virus_form").submit() if confirm
            dataType: 'json'
        false