$ ->
    prefill_info = (entry_key) ->
        $.ajax 
            url: "http://localhost:8000/api/v1/polymer"
            data:
                entry_key: entry_key
                format: 'json'
            success: (data) ->
                $.each data.objects, (index, polymer) ->
                    input = $("<input></input>").attr 
                        type: 'checkbox'
                        name: 'entity_accession_id_'+index
                       # input.append($("<p></p>").html(polymer.pdbx_description))
                    hidden_input = $("<input></input>").attr
                        type: 'hidden'
                        name: 'entity_accession_id'
                        value: polymer.pdbx_db_accession
                    $(".js-polymers").append(input)
                                     .append(hidden_input)
            error: (err) ->
                console.log err
                # TODO: Log error
            dataType: 'json'

        $.ajax
            url: "http://localhost:8000/api/v1/struct"
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
        $("label[for=id_unique_relative_id], #id_unique_relative_id")[if this.checked then "hide" else "show"]()

    $.ajax
        url: "http://localhost:8000/viruses/add_entry/start_pdbase" 
        data:
            entry_id: $('#entry_id').val()
            format: 'json'
        success: (data) ->
            prefill_info data.entry_key
            $("#virus_form").attr "hidden", not data.pdbase
            $(".message").attr "hidden", data.pdbase
        error: (err) ->
            console.log err
        dataType: 'json'