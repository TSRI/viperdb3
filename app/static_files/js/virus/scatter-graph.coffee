$ ->
    chains = _.map $("input.js-chain-id"), (chain) -> $(chain).val()
    chain_data = {}
    chain_chart = {}

    get_chain_info = (chain) ->
        $.ajax
            url: "http://localhost:8000/api/v1/residue_asa"
            data:
                format:'json'
                limit: 0
                label_asym_id: chain
                entry_key: $("#js-entry_key").val()
            success: (data) ->
                chain_data[chain] = data.objects
                update_chain(chain) 
            error: (e) ->
                console.log e
            dataType: 'json'

    get_chain_info(chain) for chain in chains

    WIDTH = 840
    HEIGHT = 300
    MARGINS =  {top: 30, right: 30, bottom: 30, left: 50}

    init_chart = () ->
        for chain in chains
            chart = d3.select("#graph-#{chain}")
                .append('svg')
                .attr('width', WIDTH)
                .attr('height', HEIGHT)

            chart.append("svg:g")
                .attr("class", "x axis")
                .attr("transform", "translate(0, #{HEIGHT-MARGINS.bottom})")

            chart.append("svg:g")
                .attr("class", "y axis")
                .attr("transform", "translate(#{MARGINS.left}, 0)")

            chain_chart["#{chain}"] = chart


    update_chain = (chain) ->
        _data = _.chain(chain_data[chain])
                .sortBy((datum) -> datum.label_seq_id)
                .map((datum) -> 
                    datum.value = (datum.radius_aa - datum.radius_min) * datum.sasa_bound
                    datum)
                .value()

        x = d3.scale.linear()
        y = d3.scale.linear()

        x.domain [0, _data.length]
        y.domain [0, d3.max(_data, (datum) -> 
            (datum.radius_aa - datum.radius_min) * datum.sasa_bound)]

        x.range [MARGINS.left, WIDTH - MARGINS.right]
        y.range [HEIGHT - MARGINS.top, MARGINS.bottom]

        xAxis = d3.svg.axis()
            .scale(x)
            .tickSize(5)
            .tickSubdivide(true)

        yAxis = d3.svg.axis()
            .scale(y)
            .tickSize(5)
            .orient("left")

        chart = chain_chart["#{chain}"]

        chart.select(".x.axis").call(xAxis)
        chart.select(".y.axis").call(yAxis)

        line = d3.svg.line()
            .x((datum) -> x(datum.label_seq_id))
            .y((datum) -> y(datum.value))

        chart.append("svg:path").attr("d", line(_data))
            .attr("fill", "transparent")
            .attr("stroke", "black")

        tip = d3.svg.tip()
            .orient("top")
            .text((datum) -> "#{datum.label_comp_id}#{datum.label_seq_id}, #{Math.round(datum.value*100)/100}")
            .attr("class", "tip")

        points = chart.selectAll('circle').data(_data, (datum) -> datum)

        points.enter()
            .append("svg:circle")
            .attr("cx", (datum) -> x(datum.label_seq_id))
            .attr("cy", (datum) -> y(datum.value))
            .attr("r", 3.5)
            .style("fill", "blue")
            .on('mouseover', tip)

    init_chart()
