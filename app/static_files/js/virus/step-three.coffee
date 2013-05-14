$ -> 
    $("#step_three_form").submit (e) ->
        e.preventDefault()
        
        formErrors = []
        $(".control-group.error").removeClass "error"
        $(".required").each (index, field) ->
            if ($(field).attr("type") is "checkbox")
                siblings = $(field).siblings ".required"
                siblings.push field
                for sibling in siblings
                    unless $(sibling).attr('checked') is undefined
                        return
                formErrors.push field 
            else if (!field.value?) or field.value is ""
                formErrors.push field

        $(formErrors).parents('.control-group').addClass "error"

        if _.isEmpty(formErrors)
            return e.currentTarget.submit()        

        false
