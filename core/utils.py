def discount_solver(product_instance):
    sum_mablagh = 0
    sum_percent = 0
    categories = product_instance.category.all()

    all_discounts = [c.discount.all() for c in categories]
    all_discounts.append(product_instance.discount.all())

    for queryset in all_discounts:
        for discount in queryset:
            limit = discount.limit
            if limit is None or limit > 0:
                if (p := discount.percent) and (m := discount.mablagh):
                    if product_instance.price * (p / 100) > m:
                        sum_mablagh += m
                    else:
                        sum_percent += p
                elif p := discount.percent:
                    sum_percent += p
                elif m := discount.mablagh:
                    sum_mablagh += m

    return sum_mablagh, sum_percent
