(function () {
    var width = document.getElementById("vote_network").clientWidth - 50,
        height = 600;

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(100)
        .size([width, height]);

    var x = d3.scale.linear()
        .domain([50, 100])
        .range([250, 80])
        .clamp(true);

    var brush = d3.svg.brush()
        .y(x)
        .extent([0, 0]);

    var svg = d3.select("#vote_network").append("svg")
        .attr("width", width)
        .attr("height", height);

    var links_g = svg.append("g");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (width - 40) + ",0)")
        .call(d3.svg.axis()
            .scale(x)
            .orient("left")
            .tickFormat(function (d) {
                return d;
            })
            .tickSize(0)
            .tickPadding(12))
        .select(".domain")
        .select(function () {
            return this.parentNode.appendChild(this.cloneNode(true));
        })
        .attr("class", "halo");

    var slider = svg.append("g")
        .attr("class", "slider")
        .call(brush);

    slider.selectAll(".extent,.resize")
        .remove();

    var handle = slider.append("circle")
        .attr("class", "handle")
        .attr("transform", "translate(" + (width - 40) + ",0)")
        .attr("r", 5);

    svg.append("text")
        .attr("x", width - 40)
        .attr("y", 60)
        .attr("text-anchor", "end")
        .attr("font-size", "12px")
        .style("opacity", 0.5)
        .text("vote the same way x% of the time");

    d3.json("https://herbertli.github.io/SenateNetwork/vgraph.json", function (error, graph) {
        if (error) throw error;

        graph.links.forEach(function (d, i) {
            d.i = i;
        });

        function brushed() {
            var value = brush.extent()[0];
            if (d3.event.sourceEvent) {
                value = x.invert(d3.mouse(this)[1]);
                brush.extent([value, value]);
            }
            handle.attr("cy", x(value));
            var threshold = value;
            var thresholded_links = graph.links.filter(function (d) {
                return ((d.value * 100) > threshold);
            });
            force.links(thresholded_links);
            var link = links_g.selectAll(".link")
                .data(thresholded_links, function (d) {
                    return d.i;
                });
            link.enter().append("line")
                .attr("class", "link");
            link.exit().remove();
            force.on("tick", function () {
                link
                    .attr("x1", function (d) {
                        return d.source.x;
                    })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });
                node.attr("transform", function (d) {
                    return "translate(" + Math.min(width - 10, d.x) + "," + Math.min(d.y, height - 10) + ")";
                });
            });
            force.start();
        }

        force.nodes(graph.nodes);
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(force.drag);
        node.append("circle")
            .attr("r", 5)
            .style("fill", function (d) {
                if (d.group === 1) return "blue";
                else if (d.group === 2) return "red";
                else return "green";
            });
        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });
        brush.on("brush", brushed);
        slider
            .call(brush.extent([5, 5]))
            .call(brush.event);
    });
})();

(function () {
    var width = document.getElementById("money_network").clientWidth - 50,
        height = 600;
    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(100)
        .size([width, height]);
    var x = d3.scale.linear()
        .domain([50, 100])
        .range([250, 80])
        .clamp(true);
    var brush = d3.svg.brush()
        .y(x)
        .extent([0, 0]);
    var svg = d3.select("#money_network").append("svg")
        .attr("width", width)
        .attr("height", height);
    var links_g = svg.append("g");
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + (width - 40) + ",0)")
        .call(d3.svg.axis()
            .scale(x)
            .orient("left")
            .tickFormat(function (d) {
                return d;
            })
            .tickSize(0)
            .tickPadding(12))
        .select(".domain")
        .select(function () {
            return this.parentNode.appendChild(this.cloneNode(true));
        })
        .attr("class", "halo");
    var slider = svg.append("g")
        .attr("class", "slider")
        .call(brush);
    slider.selectAll(".extent,.resize")
        .remove();
    var handle = slider.append("circle")
        .attr("class", "handle")
        .attr("transform", "translate(" + (width - 40) + ",0)")
        .attr("r", 5);
    svg.append("text")
        .attr("x", width - 40)
        .attr("y", 60)
        .attr("text-anchor", "end")
        .attr("font-size", "12px")
        .style("opacity", 0.5)
        .text("received donations from the same x% of industries");
    d3.json("https://herbertli.github.io/SenateNetwork/mgraph.json", function (error, graph) {
        if (error) throw error;
        graph.links.forEach(function (d, i) {
            d.i = i;
        });
        function brushed() {
            var value = brush.extent()[0];
            if (d3.event.sourceEvent) {
                value = x.invert(d3.mouse(this)[1]);
                brush.extent([value, value]);
            }
            handle.attr("cy", x(value));
            var threshold = value;
            var thresholded_links = graph.links.filter(function (d) {
                return ((d.value * 100) > threshold);
            });
            force
                .links(thresholded_links);
            var link = links_g.selectAll(".link")
                .data(thresholded_links, function (d) {
                    return d.i;
                });
            link.enter().append("line")
                .attr("class", "link")
                .style("stroke-width", function (d) {
                    return Math.sqrt(d.value);
                });
            link.exit().remove();
            force.on("tick", function () {
                link.attr("x1", function (d) {
                    return d.source.x;
                })
                    .attr("y1", function (d) {
                        return d.source.y;
                    })
                    .attr("x2", function (d) {
                        return d.target.x;
                    })
                    .attr("y2", function (d) {
                        return d.target.y;
                    });
                node.attr("transform", function (d) {
                    return "translate(" + Math.min(width - 10, d.x) + "," + Math.min(d.y, height - 10) + ")";
                });
            });
            force.start();
        }

        force.nodes(graph.nodes);
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(force.drag);
        node.append("circle")
            .attr("r", 5)
            .style("fill", function (d) {
                if (d.group === 1) return "blue";
                else if (d.group === 2) return "red";
                else return "green";
            });
        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });
        brush.on("brush", brushed);
        slider
            .call(brush.extent([5, 5]))
            .call(brush.event);
    });
})();
