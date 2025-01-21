odoo.define('garantias.garantia_map', function (require) {
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const rpc = require('web.rpc');

    const GarantiasMapView = AbstractAction.extend({
        start: function () {
            // Crear contenedor HTML para el mapa
            this.$el.append("<div id='garantias_map' style='width:100%; height:600px;'></div>");

            // Obtener la clave de Google Maps desde el servidor Odoo
            return rpc.query({
                route: '/garantias/get_api_key',
            }).then((data) => {
                const googleApiKey = data.api_key;
                if (!googleApiKey) {
                    console.error("No se pudo obtener la API Key de Google Maps.");
                    return;
                }

                // Cargar el script de Google Maps dinámicamente
                let script = document.createElement('script');
                script.src = `https://maps.googleapis.com/maps/api/js?key=${googleApiKey}&callback=initGarantiasMap`;
                document.head.appendChild(script);
            }).catch((err) => {
                console.error("Error obteniendo la API Key de Google Maps:", err);
            });
        },
    });

    window.initGarantiasMap = function () {
        rpc.query({
            model: 'res.company',
            method: 'get_parent_company_location',
            args: [],
        }).then((companyLocation) => {
            const center = companyLocation?.lat && companyLocation?.lng
                ? { lat: companyLocation.lat, lng: companyLocation.lng }
                : { lat: 40.416775, lng: -3.703790 };  // Madrid por defecto

            const map = new google.maps.Map(document.getElementById("garantias_map"), {
                zoom: 6,
                center: center,
            });

            // Obtener coordenadas de las garantías registradas
            return rpc.query({
                model: 'garantias',
                method: 'search_read',
                args: [
                    [],
                    ['latitude', 'longitude', 'name']
                ],
            }).then((results) => {
                results.forEach((garantia) => {
                    if (garantia.latitude && garantia.longitude) {
                        new google.maps.Marker({
                            position: {
                                lat: garantia.latitude,
                                lng: garantia.longitude
                            },
                            map: map,
                            title: garantia.name,
                        });
                    }
                });
            });

        }).catch((err) => {
            console.error("Error obteniendo la ubicación de la compañía:", err);
            new google.maps.Map(document.getElementById("garantias_map"), {
                zoom: 6,
                center: { lat: 40.416775, lng: -3.703790 },
            });
        });
    };

    core.action_registry.add('garantias_map_view', GarantiasMapView);

    return GarantiasMapView;
});