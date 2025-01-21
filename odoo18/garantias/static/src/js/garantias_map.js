odoo.define('garantias.MapView', function (require) {
    "use strict";

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');
    const rpc = require('web.rpc');

    const GarantiasMapView = AbstractAction.extend({
        /**
         * Este método se llama cuando se abre la acción 'garantias_map_view'.
         */
        start: function () {
            // 1) Crear contenedor HTML para el mapa
            this.$el.append("<div id='garantias_map' style='width:100%; height:600px;'></div>");

            // 2) Obtener latitud y longitud de la compañía padre del usuario activo
            return rpc.query({
                model: 'res.company',
                method: 'get_parent_company_location',
                args: [],
            }).then((companyLocation) => {
                // 3) Establecer el centro del mapa basado en la ubicación de la compañía o Madrid por defecto
                const center = companyLocation && companyLocation.lat && companyLocation.lng
                    ? { lat: companyLocation.lat, lng: companyLocation.lng }
                    : { lat: 40.416775, lng: -3.703790 };  // Madrid por defecto

                // Inicializar el mapa con la ubicación obtenida
                const map = new google.maps.Map(document.getElementById("garantias_map"), {
                    zoom: 6,
                    center: center,
                });

                // 4) Llamar al backend para obtener las coordenadas de las garantías registradas
                return rpc.query({
                    model: 'garantias',
                    method: 'search_read',
                    args: [
                        [],
                        ['latitude', 'longitude', 'name'] // campos a recuperar
                    ],
                }).then((results) => {
                    // 5) Recorrer los registros y agregar marcadores en el mapa
                    results.forEach((garantia) => {
                        if (garantia.latitude && garantia.longitude) {
                            const marker = new google.maps.Marker({
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
                // Si hay error, mostrar el mapa en la ubicación por defecto (Madrid)
                const map = new google.maps.Map(document.getElementById("garantias_map"), {
                    zoom: 6,
                    center: { lat: 40.416775, lng: -3.703790 },
                });
            });
        },
    });

    core.action_registry.add('garantias_map_view', GarantiasMapView);

    return GarantiasMapView;
});