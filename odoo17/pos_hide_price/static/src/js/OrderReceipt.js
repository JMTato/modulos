import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/order_receipt";

patch(OrderReceipt.prototype, "pos_receipt_hide_price.OrderReceipt", {
    setup() {
        super.setup();
    },

    get priceHidden() {
        return this.props.hidePriceState?.priceHidden ?? false;
    }
});