import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

patch(ReceiptScreen.prototype, "pos_receipt_hide_price.ReceiptScreen", {
    setup() {
        super.setup();
        this.hidePriceState = useState({ priceHidden: false });
    },

    hidePrice() {
        this.hidePriceState.priceHidden = !this.hidePriceState.priceHidden;
    },

    get priceHidden() {
        return this.hidePriceState.priceHidden;
    }
});