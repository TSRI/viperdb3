$ ->
    $("#virus-images").carouFredSel
        items: 
            start: 0
            visible: 3
            width: 200
            height: 200
            filter: "img"
        circular: false
        infinite: false
        auto: false
        width: 760
        height: 200
        prev:
            button: "section#illustrations #prev-image"
        next:
            button: "section#illustrations #next-image"
        scroll:
            items: 3
