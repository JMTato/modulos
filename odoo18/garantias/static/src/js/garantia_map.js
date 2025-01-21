/** @odoo-module **/

import AbstractAction from 'web.AbstractAction';
import core from 'web.core';
import rpc from 'web.rpc';

class GarantiasMapView extends AbstractAction {
    async start() {
        this.$el.append("<div id='garantias_map' style='width:100%; height:600px;'></div>");

        try {
            const data = await rpc.query({
                route: '/garantias/get_api_key',
            });

            const googleApiKey = data.api_key;
            if (!googleApiKey) {
                console.error("No se pudo obtener la API Key de Google Maps.");
                return;
            }

            let script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=${googleApiKey}&callback=initGarantiasMap`;
            document.head.appendChild(script);
        } catch (err) {
            console.error("Error obteniendo la API Key de Google Maps:", err);
        }
    }
}

window.initGarantiasMap = async function () {
    try {
        const companyLocation = await rpc.query({
            model: 'res.company',
            method: 'get_parent_company_location',
            args: [],
        });

        const center = companyLocation?.lat && companyLocation?.lng
            ? { lat: companyLocation.lat, lng: companyLocation.lng }
            : { lat: 40.416775, lng: -3.703790 }; // Madrid por defecto

        const map = new google.maps.Map(document.getElementById("garantias_map"), {
            zoom: 6,
            center: center,
        });

        const results = await rpc.query({
            model: 'garantias',
            method: 'search_read',
            args: [[], ['latitude', 'longitude', 'name']],
        });

        results.forEach((garantia) => {
            if (garantia.latitude && garantia.longitude) {
                new google.maps.Marker({
                    position: {
                        lat: garantia.latitude,
                        lng: garantia.longitude,
                    },
                    map: map,
                    title: garantia.name,
                });
            }
        });
    } catch (err) {
        console.error("Error obteniendo la ubicación de la compañía o garantías:", err);
        new google.maps.Map(document.getElementById("garantias_map"), {
            zoom: 6,
            center: { lat: 40.416775, lng: -3.703790 },
        });
    }
};

core.action_registry.add('garantias_map_view', GarantiasMapView);

export default GarantiasMapView;
