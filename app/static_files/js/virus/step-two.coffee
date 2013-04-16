$ ->
    prefill_info = (entry_key) ->
        $.ajax 
            url: "/api/v1/polymer"
            data:
                entry_key: entry_key
                format: 'json'
            success: (data) ->
                $.each data.objects, (index, polymer) ->
                    input = $("<input></input>").attr 
                        type: 'checkbox'
                        name: 'entity_accession_id_'+index
                    hidden_input = $("<input></input>").attr
                        type: 'hidden'
                        name: 'entity_accession_id'
                        value: polymer.pdbx_db_accession
                    $(".js-polymers").append(input)
                                     .append(hidden_input)
                    input.after($("<p></p>").html(polymer.pdbx_description))
            error: (err) ->
                console.log err
                # TODO: Log error
            dataType: 'json'

        $.ajax
            url: "/api/v1/struct"
            data:
                entry_key: entry_key
                format: 'json'
            success: (data) ->
                virus = data.objects[0]
                $("#id_deposition_date").val virus.entry_key.deposition_date
                $("#id_name").val virus.title
            dataType: 'json'

        $("#virus_form").attr 'hidden', false

    $('.formset').formset
        prefix: '{{ layer_formset.prefix }}'

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

        # $(".required").each(function(index,field) {
        #     if(field.value == null || field.value == "")
        #     {
        #         field.className.parent().parent().addClass("error");
        #     }
        # })
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
