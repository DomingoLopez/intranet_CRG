export interface MenuElement {
    id_menu:            string;
    label:              string;
    categoria:          string;
    tipo_activo:        string;
    url:                string;
    order:              number;
    permitir_fav:       Boolean;
    is_fav:             Boolean;
    ruta:               string;
    childs:             MenuElement[];
}


export enum TipoEnlace {
    HUB = "hub",
    SUBMENU = "submenu",
    WEBFOCUS = "informe_webfocus",
}
