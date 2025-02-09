/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, onRendered } from "@odoo/owl";

class GarantiasMapView extends Component {
    static template = "garantias.GarantiasMapView";

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.map = null;
        this.garantias = [];

        onMounted(async () => {
            console.log("Componente montado, cargando datos...");
            await this.loadGarantias();  // Carga de datos al montar
        });
        
        onRendered(() => {
            console.log("El componente ha sido renderizado, verificando mapa...");
            
            const checkMapContainer = (attempts = 0) => {
                if (attempts >= 20) {
                    console.error("No se pudo inicializar el mapa, el contenedor no está disponible.");
                    return;
                }
        
                requestAnimationFrame(() => {
                    if (this.el) {
                        const mapContainer = this.el.querySelector("#garantias_map");
                        if (mapContainer) {
                            console.log("Contenedor del mapa encontrado, inicializando...");
                            this.initMap();
                        } else {
                            console.warn(`Intento ${attempts + 1}: El contenedor del mapa aún no está disponible, reintentando...`);
                            setTimeout(() => checkMapContainer(attempts + 1), 500);
                        }
                    } else {
                        console.warn(`this.el aún es undefined, reintentando intento ${attempts + 1}...`);
                        setTimeout(() => checkMapContainer(attempts + 1), 500);
                    }
                });
            };
        
            checkMapContainer();
        });
    }
    async loadGarantias() {
        try {
            console.log("Intentando cargar garantías...");
            this.garantias = await this.orm.searchRead("garantias",
                [['latitude', '!=', false], ['longitude', '!=', false]],
                ['latitude', 'longitude', 'name']
            );
    
            if (!Array.isArray(this.garantias) || this.garantias.length === 0) {
                console.warn("No se encontraron garantías para mostrar en el mapa.");
                return;
            }
    
            this.garantias = this.garantias.filter(garantia => {
                if (typeof garantia.latitude !== 'string' || typeof garantia.longitude !== 'string') {
                    console.error(`Datos inválidos en garantía: ${garantia.name}`);
                    return false;
                }
                return true;
            });
    
            console.log("Garantías cargadas con éxito:", this.garantias);
        } catch (error) {
            console.error("Error al cargar garantías:", error);
        }
    }

    ensureMapContainer(attempts = 0) {
        if (attempts >= 20) {
            console.error("No se pudo encontrar el contenedor del mapa después de varios intentos.");
            return;
        }
    
        requestAnimationFrame(() => {
            if (this.el) {
                const mapContainer = this.el.querySelector("#garantias_map");
                if (mapContainer) {
                    this.initMap();
                } else {
                    console.warn(`Intento ${attempts + 1}: El elemento del mapa no está disponible aún.`);
                    this.ensureMapContainer(attempts + 1);
                }
            } else {
                console.error("this.el aún no está definido, reintentando...");
                this.ensureMapContainer(attempts + 1);
            }
        });
    }

    initMap() {
        const mapContainer = this.el?.querySelector("#garantias_map");
        if (!mapContainer) {
            console.error("No se encontró el contenedor del mapa en la plantilla.");
            return;
        }
    
        if (this.map) {
            console.warn("El mapa ya ha sido inicializado.");
            return;
        }
    
        this.map = L.map(mapContainer).setView([0, 0], 2);  // Vista inicial centrada en el mundo
    
        // Añadir control de zoom en la esquina superior derecha
        L.control.zoom({ position: 'topright' }).addTo(this.map);
    
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
    
        let bounds = L.latLngBounds();
    
        this.garantias.forEach(garantia => {
            const lat = parseFloat(garantia.latitude);
            const lon = parseFloat(garantia.longitude);
            if (!isNaN(lat) && !isNaN(lon) && lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180) {
                L.marker([lat, lon])
                    .addTo(this.map)
                    .bindPopup(`<b>${garantia.name}</b>`);
                bounds.extend([lat, lon]);
            } else {
                console.warn(`Coordenadas no válidas para: ${garantia.name}`);
            }
        });
    
        if (bounds.isValid()) {
            this.map.fitBounds(bounds, { padding: [50, 50] });
            if (this.garantias.length === 1) {
                this.map.setZoom(15);
            }
        } else {
            console.warn("No hay ubicaciones válidas para mostrar en el mapa.");
        }
    }
}
registry.category("actions").add("garantias_map_view", GarantiasMapView);