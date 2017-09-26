(function (global, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['lib/jquery-1.8.2.min'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS
  } else {
    // Browser globals
    global.AppMap = factory(jQuery);
  }
}((this.self || global), function ($) {
  'use strict';

  var AppMap = function() {
    Materialize.updateTextFields();
    $(".datepicker").pickadate({
      selectMonths: true,
      selectYear: 15,
      selectYears: true,
      selectMonths: true,
      format: 'yyyy-mm-dd',
      onClose: function() {
        $("#search_button").click();
	  }
    });
  };

  AppMap.prototype = {
    constructor: AppMap,
    init: function() {
      this.map = this.initMap('map');
      this.initDrawRect();
      this.initModal();
      this.initMapEvent();
      this.initCountrySelect();
      this.bindButtons();
      this.miniMap = this.initMap('mini_map');
    },
    initMap: function(id) {
      var vectorSource = new ol.source.Vector({wrapX: false});
      var vector = new ol.layer.Vector({
        source: vectorSource
      });
      var tile = new ol.layer.Tile({
        source: new ol.source.OSM()
      });
	  if (id == "map") {
	    this.vectorSource = vectorSource;
	  }
      return new ol.Map({
        layers: [tile,vector],
        target: id,
        view: new ol.View({
          center: [-11000000, 4600000],
          zoom: 3
        })
      });
    },
    initDrawRect: function() {
      var self = this;
      this.collection = new ol.Collection();
      this.draw = new ol.interaction.Draw({
        source: self.vectorSource,
        type: 'Circle',
        features: this.collection,
        freehandCondition: ol.events.condition.always,
        geometryFunction: ol.interaction.Draw.createBox()
      });
      this.draw.on('drawend', function(e) {
        var rect = ol.proj.transformExtent( e.feature.getGeometry().getExtent(), 'EPSG:3857', 'EPSG:4326' );
        self.setGeo(rect);
      });
    },
    initModal: function() {
      $("#map_search_modal").modal();
    },
    initMapEvent: function() {
      var self = this;
      this.enablePointerMove = false
      this.map.on('pointermove', function(evt) {
        if (evt.dragging) return;
        if (!self.enablePointerMove) return;
        var pixel = self.map.getEventPixel(evt.originalEvent);
        self.displayFeatureInfo(pixel, evt);
      });
      this.map.on('click', function(evt) {
        if (!self.enablePointerMove) return;
        var pixel = self.map.getEventPixel(evt.originalEvent);
        var feature = self.map.forEachFeatureAtPixel(pixel, function(feature) {
          return feature;
        });
        var rect = ol.proj.transformExtent(feature.getGeometry().getExtent(), 'EPSG:3857', 'EPSG:4326' );
        if (feature.getId() == "RUS") {
          rect = [18.53284749453115, 41.097478598193334, 190.79847249453115,81.33184651684658];
        }
        self.setGeo(rect)
        $("#search_button").click();
      });
    },
    initCountrySelect: function() {
      var style = new ol.style.Style({
        fill: new ol.style.Fill({
          color: 'rgba(0,0,0,0)'
        }),
        stroke: new ol.style.Stroke({
          color: 'rgba(0,0,0,0)',
          width: 0
        }),
        text: new ol.style.Text({
          font: '12px Calibri,sans-serif',
          fill: new ol.style.Fill({
            color: '#000'
          }),
          stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3
          })
        })
      });

      this.countriesLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
          url: 'https://openlayers.org/en/v3.20.1/examples/data/geojson/countries.geojson',
          format: new ol.format.GeoJSON()
        }),
        style: function(feature, resolution) {
          style.getText().setText(resolution < 5000 ? feature.get('name') : '');
          return style;
        }
      });

      var highlightStyleCache = {};
      this.featureOverlay = new ol.layer.Vector({
        source: new ol.source.Vector(),
        style: function(feature, resolution) {
          var text = resolution < 5000 ? feature.get('name') : '';
          if (!highlightStyleCache[text]) {
            highlightStyleCache[text] = new ol.style.Style({
              stroke: new ol.style.Stroke({
                color: '#f00',
                width: 1
              }),
              fill: new ol.style.Fill({
                color: 'rgba(255,0,0,0.1)'
              }),
              text: new ol.style.Text({
                font: '12px Calibri,sans-serif',
                text: text,
                fill: new ol.style.Fill({
                  color: '#000'
                }),
                stroke: new ol.style.Stroke({
                  color: '#f00',
                  width: 3
                })
              })
            });
          }
          return highlightStyleCache[text];
        }
      });
      this.highlight = null;
    },
    displayFeatureInfo: function(pixel, evt) {
      var feature = this.map.forEachFeatureAtPixel(pixel, function(feature) {
        return feature;
      });
      if (feature) {
        var name = feature.get('name');
        $("#popover").css({
          "left": evt.originalEvent.x + 5,
          "top": evt.originalEvent.y + 5,
        }).text(name).show();
      } else {
        $("#popover").hide();
      }
      if (feature !== this.highlight) {
        if (this.highlight) {
          this.featureOverlay.getSource().removeFeature(this.highlight);
        }
        if (feature) {
          this.featureOverlay.getSource().addFeature(feature);
        }
        this.highlight = feature;
      }
    },
    bindButtons: function() {
      var self = this;
      $(".drawButton").on("click", function() {
        self.map.unByKey("click", null);
        this.enablePointerMove = false;
        $("#popover").hide();
        self.map.removeLayer(self.countriesLayer);
        self.map.removeLayer(self.featureOverlay);
        $(".clickButton").removeClass("darken-4");

        if ($(this).hasClass("darken-4")) {
          $(this).removeClass("darken-4");
          self.map.removeInteraction(self.draw);
        } else {
          $(this).addClass("darken-4");
          self.map.addInteraction(self.draw);
        }
      });

      $(".searchButton").on("click", function() {
        $("#map_search_modal").modal("open");
      });

      $(".deleteButton").on("click", function() {
        self.clearSelected();
      });

      $(".clickButton").on("click", function() {
        self.map.removeInteraction(self.draw);
        $(".drawButton").removeClass("darken-4");

        if ($(this).hasClass("darken-4")) {
          $(this).removeClass("darken-4");
          self.map.unByKey("click");
          self.enablePointerMove = false;
          $("#popover").hide();
          self.map.removeLayer(self.countriesLayer);
          self.map.removeLayer(self.featureOverlay);
        } else {
          self.map.addLayer(self.countriesLayer);
          self.map.addLayer(self.featureOverlay);
          $(this).addClass("darken-4");
          self.enablePointerMove = true;
        }
      });

	  $(".miniDrawButton").on("click", function() {
        $("#big_map").show();
		$("#mini_map_wrapper").hide();
      });

	  $(".closeButton").on("click", function() {
        $("#big_map").hide();
		$("#mini_map_wrapper").show();
	  });

      var suggestTimer = null;
      $("#mapq").on("keyup", function() {
        clearTimeout(suggestTimer);
        var query = $(this).val();
        suggestTimer = setTimeout(function() {
          self.suggestSearch(query);
        }, 500);
      });
    },
    drawRect: function(geo) {
      this.layerPolygon = null
      var feature = new ol.Feature({
        geometry: new ol.geom.Polygon(geo.coordinates)
      });
      feature.getGeometry().transform('EPSG:4326', 'EPSG:3857');
      this.layerPolygon = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: [feature]
        })
      });
      this.map.addLayer(this.layerPolygon);
      var extent = feature.getGeometry().getExtent();
      var center = [(extent[0]+extent[2])/2, (extent[1]+extent[3])/2];
      this.map.getView().setCenter(center);
      this.map.getView().fit(extent, this.map.getSize());

      var feature = new ol.Feature({
        geometry: new ol.geom.Polygon(geo.coordinates)
      });
      feature.getGeometry().transform('EPSG:4326', 'EPSG:3857');
      var layerPolygon = new ol.layer.Vector({
        source: new ol.source.Vector({
          features: [feature]
        })
      });
      this.miniMap.addLayer(layerPolygon);
      var extent = feature.getGeometry().getExtent();
      var center = [(extent[0]+extent[2])/2, (extent[1]+extent[3])/2];
      this.miniMap.getView().setCenter(center);
      this.miniMap.getView().fit(extent, this.miniMap.getSize());
    },
    clearSelected: function() {
      if (this.collection.getLength() >= 1) {
        var remove = this.collection.pop();
        this.vectorSource.removeFeature(remove);
      }
      if (this.layerPolygon) {
        this.map.removeLayer(this.layerPolygon);
        this.layerPolygon = null;
      }
      $("[name=geo]").val("")
    },
    setGeo: function(rect) {
      var coordinates = [[
        [rect[0], rect[1]],
        [rect[2], rect[1]],
        [rect[2], rect[3]],
        [rect[0], rect[3]],
        [rect[0], rect[1]]
      ]];
      this.clearSelected();
      $("[name=geo]").val(JSON.stringify({type: "Polygon", coordinates: coordinates}))
    },
    suggestSearch: function(query) {
      var self = this;
      $.ajax({
        data: "q=" + encodeURIComponent(query),
        url: "/map_suggest",
        dataType:"json",
        success: function(data) {
          var c = $(".map_candidates")
          c.empty()
          data.forEach(function(d) {
            var tr = $("<tr/>").append(
              $("<td/>")
                .text(d.name)
                .on("click", function() {
                  self.setGeo(d.loc);
                  $("#search_button").click();
                })
            );
            c.append(tr)
          });
        },
      });
    }
  };
  return AppMap;
}));
