/**
 * Created by Iven on 2016/10/19.
 */

$(document).ready(function () {
    $(function(){
        // 创建图表
        function createChartA(conf){
            console.log(conf)
            $(conf.selector).kendoChart({
                legend: {
                   position: "bottom"
                },
                theme : 'bootstrap',
                seriesDefaults: {
                    labels: {
                        template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                        position: "outsideEnd",
                        visible: true,
                        background: "transparent"
                    }
                },
                series: [{
                    type: conf.type,
                    data: conf.data.series
                }],
                tooltip: {
                    visible: true,
                    template: "#= category # - #= kendo.format('{0:P}', percentage) #"
                }
            });
        }

        // 异步请求后台数据
        $.ajax({
            url: site_url+'get_server_system/',
            type: 'GET',
            dataType: 'json',
            success: function(res){
                createChartA({
                    selector: "#chartA", // 图表窗器
                    type: "pie", // 图表类型
                    data: res // 图表数据
                });
            }
        });
        //charts_pie_demo1_js_end
    });

    $(function(){
        // 创建图表
        function createChartB(conf){
            $(conf.selector).kendoChart({
                legend: {
                    position: "bottom"
                },
                theme : 'bootstrap',
                seriesDefaults: {
                    type: "line",
                    style: "smooth",
                    labels: {
                        position: "outsideEnd",
                        visible: true,
                    }
                },
                series: conf.data.series,
                categoryAxis: {
                    majorGridLines : {
                        visible: false
                    },
                    categories: conf.data.categories,
                    labels: {
                        rotation: "auto"
                    },
                },
                tooltip: {
                    visible: true,
                    template: "【#= category #】 #= value #"
                }
            });
            //重新绘制
            $(window).on('resize',function(){
                var chart = $(conf.selector).data("kendoChart");
                chart.redraw();
            });

        }

        function initChart(conf){
            // 异步请求后台数据
            $.ajax({
                url: conf.url,
                type: 'GET',
                dataType: conf.dataType,
                success: function(res){
                    var series = [{'name': conf.name, 'data': res.data.health_check_list, 'color': '#00DB00'}];
                    var categories = res.data.date_list;

                    createChartB({
                        selector: conf.container, // 图表窗器
                        type: "line", // 图表类型
                        data: {'series': series, 'categories': categories} // 图表数据
                    });
                    //setTimeout(initChart(conf),10000);
                }
            });
        }

        initChart({
            url: site_url+'get_record_list/',
            dataType: 'json',
            name: "Linux健康检查次数",
            container: '#chartB'
        });

    });


});


