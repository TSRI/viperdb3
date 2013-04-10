$ ->
    $("#id_unique").on 'click', () ->
        $("label[for=unique_relative], #id_unique_relative")[if this.checked then "hide" else "show"]()

    $.ajax
        url: "/admin/add_entry/start_pdbase" 
        data:
            entry_id: $('#entry_id').attr "value"
            format: 'json'
        success: (data) ->
            prefill_info data.entry_key
            $("#virus_form").attr "hidden", not data.pdbase
            $(".message").attr "hidden", data.pdbase
        error: (err) ->
            console.log err
        dataType: 'json'

    $("virus_form").submit ->
        boxes = $("span.js-polymers input[type='checkbox']")
        _.some boxes, (checkbox) ->
            checkbox.attr "checked"

        