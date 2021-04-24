AVITO_START_XPATH = '//a[(contains(@class, "rubricator-list-item-link")) and (@data-marker="category[1000030]/link")]/@href'

AVITO_PAGE_XPATH = {
    "pagination": '//div[@class="pagination-pages clearfix"]/'
                  'a[@class="pagination-page"]/@href',
    "apartment": '//div[contains(@class,"items-items") and contains(@data-marker,"catalog-serp")]//'
                 'div[contains(@class,"iva-item-titleStep")]/a[@data-marker="item-title"]/@href',
}

AVITO_APARTMENT_XPATH = {
    "title": '//div[contains(@class,"item-view-title-info")]//'
             'span[@class="title-info-title-text"]/text()',
    "price": '//span[contains(@class,"price-value-string")]//'
             'span[@class="js-item-price"]/@content',
    "address": '//div[@itemprop="address"]/span[@class="item-address__string"]/text()',
    "description": '//div[@class="item-params"]//ul[@class="item-params-list"]/li//text()',
    "seller": '//div[contains(@class,"item-view-seller-info")]//div[@data-marker="seller-info/name"]/a[1]/@href',
    "name": '//div[@data-marker="seller-info/name"]/a/text()',
}

AVITO_SELLER_ID = '//div[@data-marker="seller-info/name"]/a/@href'