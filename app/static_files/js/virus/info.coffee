$(document).ready ->

    $(".fancybox-thumb").fancybox
        prevEffect: 'none'
        nextEffect: 'none'

        closeBtn: false
        arrows: false
        nextClick: true

        helpers:
            thumbs:
                width: 100
                height: 100
    
    $("#virus-images").carouFredSel
        items: 
            start: 0
            visible: 3
            width: 150
            height: 150
            filter: "img"
        circular: false
        infinite: false
        auto: false
        width: 640 
        height: 150
        prev:
            button: "section#illustrations #prev-image"
        next:
            button: "section#illustrations #next-image"
        scroll:
            items: 3
