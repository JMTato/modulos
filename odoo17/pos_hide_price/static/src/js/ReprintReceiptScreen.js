import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { ReprintReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/reprint_receipt_screen";

patch(ReprintReceiptScreen.prototype, "pos_receipt_hide_price.ReprintReceiptScreen", {
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