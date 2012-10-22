$ ->
    chain_data = []
    chain_count = 0
    chart = {}
    RESIDUE_TYPE = {}

    init_handlers = () ->
        $("#js-color-by-chain").on 'click',        () -> color_residues('chain')
        $("#js-color-by-identity").on 'click',     () -> color_residues('identity')
        $("#js-color-by-SASA").on 'click',         () -> color_residues('sasa')
        $("#js-color-by-interactions").on 'click', () -> color_residues('interactions')
        $("#js-residue_type").on 'change',         () -> filter_residues($(this).val())
        $("#js-select-interface").on 'click',      () -> query_chains("INTERFACE")
        $("#js-select-core").on 'click',           () -> query_chains("CORE")
        $("#js-select-surfout").on 'click',        () -> query_chains("SURFOUT")
        $("#js-select-surfin").on 'click',         () -> query_chains("SURFIN")

    filter_residues = (filter_on) ->
        points = chart.selectAll('.residues')
        if filter_on == 'ALL'
            points.style('opacity', 1)
        else
            points.each((datum, index) -> 
                opacity = if datum.ci != filter_on then 0 else 1
                d3.select(this).style('opacity', opacity) 
            )

    color_residues = (color_by) ->
        sort_sasa = (datum) ->
            if datum.sasa <= MAX_SASA / 3
                COLOR_DICT['A']
            else if datum.sasa <= MAX_SASA * 2 /3
                COLOR_DICT['C']
            else if datum.sasa <= MAX_SASA
                COLOR_DICT['B']

        sort_identity = (datum) -> 
            switch datum.cons
                when '-' then COLOR_DICT['A']
                when ':' then COLOR_DICT['C']
                when '*' then COLOR_DICT['B']

        sort_chain = (datum) -> 
            COLOR_DICT[datum.ai]

        sort_interactions = (datum) ->
            if datum.num_int <= 2
                COLOR_DICT['A']
            else if datum.num_int <= 4
                COLOR_DICT['C']
            else if datum.num_int > 4
                COLOR_DICT['B']

        points = chart.selectAll('circle')
        points.attr('stroke', 'black')
        points.attr('fill', (datum) -> 
            switch color_by
                when "chain"        then sort_chain datum
                when "identity"     then sort_identity datum
                when "sasa"         then sort_sasa datum
                when "interactions" then sort_interactions datum
        )

    get_cartesian = (residue) ->
        deg_to_rad = Math.acos(-1) / 180
        residue['x'] = (225*Math.cos(residue.phi*deg_to_rad)*Math.sin(residue.psi*deg_to_rad))+256
        residue['y'] = -((440*Math.sin(residue.phi*deg_to_rad)*Math.sin(residue.psi*deg_to_rad)-512) / 2)
        return residue

    query_chains = (SIC) ->
        $.ajax
            url: "http://localhost:8000/api/v1/atom_site/"
            data:
                format: 'json'
                entry_key: $("#js-entry_key").val()
            success: (data) ->
                chain_data = []
                chain_count = data.objects.length
                _.each data.objects, (datum) -> get_chain_info datum.label_asym_id, SIC
            error: (e) ->
                console.log "Error: #{e}"
            dataType:'json'

    get_chain_info = (chain, SIC) ->
        $.ajax
            url: "http://localhost:8000/api/v1/phi_psi/"
            data:
                format:'json'
                label_asym_id: chain 
                entry_key: $("#js-entry_key").val()
                sic: SIC
            success: (data) ->
                chain_data.push data.objects
                if chain_data.length == chain_count
                    _.each chain_data, get_cartesian
                    init_chains()
                    color_residues('chain')
                    update_chains()
            error: (e) ->
                console.log "Error: #{e}"
            dataType: 'json'

    WIDTH   = 500 
    HEIGHT  = 500
    MARGINS = {top: 30, right: 30, bottom: 30, left: 50}
    COLOR_DICT = {A: "blue", B: "red", C: "green"}
    MAX_SASA = 0
    UNIT_DATA = [{phi:0, psi:-21}, {phi:0, psi:21}, {phi:90, psi:32}]
    _.each UNIT_DATA, get_cartesian

    zoomLevel = 1
    down = false
    mouseStart = [0,0]
    posX = 0
    posY = 0
    chartX = 0 #chartX and chartY are used for mouse translations 
    chartY = 0
    translateX = 0 #translateX and translateY are used for zoom translations
    translateY = 0
    triangleWidth = d3.max(UNIT_DATA, (d) -> d.x) - d3.min(UNIT_DATA, (d) -> d.x)
    triangleHeight = d3.max(UNIT_DATA, (d) -> d.y) - d3.min(UNIT_DATA, (d) -> d.y) 
    baseCoords = [(WIDTH - triangleWidth)/2 + MARGINS.left,  d3.min(UNIT_DATA, (d) -> d.y)]

    x = d3.scale.linear()
    y = d3.scale.linear()
    tip = d3.svg.tip()
        .orient("top")
        .text((datum) -> "#{datum.ci} #{datum.si}")
        .attr("class", "tip")
        .offset(() -> [posX, posY])

    mousemove = () ->
        if down
            mouse = d3.svg.mouse(chart[0][0])
            posX = chartX + mouse[0] - mouseStart[0]
            posY = chartY + mouse[1] - mouseStart[1]
            update_position()

    mouseup = () ->
        down = false
        chartX = posX
        chartY = posY

    mousedown = () ->
        down = true
        mouseStart = d3.svg.mouse(chart[0][0])

    showInformation = (residue) ->
        $("#js-information").text("#{residue.ci} #{residue.si} # of Interactions: #{residue.num_int}")

    update_position = () ->
        graph = chart.selectAll('.residues, .triangle, .tip')
        graph.attr('transform', "translate(#{posX}, #{posY})")

    init_chart = () ->
        chart = d3.select("#graph").append('svg')
            .attr('width', WIDTH)
            .attr('height', HEIGHT)
            .call(d3.behavior.zoom().scaleExtent([0.2, 10]).on("zoom", update_chains))
            .on("mousemove", mousemove)
            .on("mouseup", mouseup)
            .on("mousedown", mousedown)

        x.domain [d3.min(UNIT_DATA, (d) -> d.x), d3.max(UNIT_DATA, (d) -> d.x)]
        y.domain [d3.min(UNIT_DATA, (d) -> d.y), d3.max(UNIT_DATA, (d) -> d.y)]

        triangle_path = chart.selectAll('.triangle').data(UNIT_DATA, (datum) -> datum)
        triangle_path.enter().append("path")
            .attr("class", "triangle")
            .style("stroke-width", 2)
            .style("stroke", "lightsteelblue")
            .style("fill", "none")

    init_chains = () ->
        _data = _.reduce chain_data, ((accum, chain) -> accum.concat(chain)), []

        points = chart.selectAll('circle').data(_data, (datum) -> datum)
        points.enter().append('svg:circle')
            .attr('r', 7)
            .attr("class", "residues")
        points.exit().remove()

        MAX_SASA = _.max [MAX_SASA, _.chain(_data).pluck('sasa').max().value()]

    update_chains = (zoom) ->
        if d3.event?
            zoomLevel = d3.event.scale 
            translateX = d3.event.translate[0] 
            translateY = d3.event.translate[1] 

        x.range  [d3.min(UNIT_DATA, (d) -> d.x)*-zoomLevel, d3.max(UNIT_DATA, (d) -> d.x)*zoomLevel]
        y.range  [d3.min(UNIT_DATA, (d) -> d.y)*-zoomLevel, d3.max(UNIT_DATA, (d) -> d.y)*zoomLevel]

        points = chart.selectAll('circle')
            .attr('cx', (datum) -> x(datum.x))
            .attr('cy', (datum) -> y(datum.y))
            # .on("mouseover", tip)
            .on("mousedown", tip)
            # .on("mousedown", showInformation)

        tip.attr("width", 500)

        line = d3.svg.line().interpolate('linear')
            .x((datum) -> x(datum.x))
            .y((datum) -> y(datum.y))
        triangle_path = chart.selectAll('.triangle')
            .attr('d', line(UNIT_DATA) + "Z")

        posX = baseCoords[0] * zoomLevel + translateX
        posY = baseCoords[1] * zoomLevel + translateY
        update_position()

    init_chart()
    init_handlers()
    query_chains('INTERFACE')