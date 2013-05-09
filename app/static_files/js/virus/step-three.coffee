$ -> 
    $("#step_three_form").submit (e) ->
        e.preventDefault()
        $(".required").each (index, field) ->
            error = false
            if ($(field).attr("type") is "checkbox")
                siblings = $(field).siblings ".required"
                siblings.push(field)
                for sibling in siblings
                    unless $(sibling).attr('checked') is undefined
                        return
                error = true
            else if (!field.value?) or field.value is ""
                error = true
            if error
                $(field).parents('.control-group').addClass "error"
            else
                $(field).parents('.control-group').removeClass "error"
        unless error
            e.currentTarget.submit()        
        not error
