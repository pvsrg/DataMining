HH_PAGE_XPATH = {
    "vacancy": '//div[@data-qa="vacancy-serp__results"]'
               '//a[@data-qa="vacancy-serp__vacancy-title"]/@href',
    "company": '//div[@data-qa="vacancy-serp__results"]'
               '//a[@data-qa="vacancy-serp__vacancy-employer"]/@href',
    "pagination": '//div[@data-qa="pager-block"]//'
                  'a[@class="bloko-button"]/@href',
}

HH_VACANCY_XPATH = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "skills": '//div[@class="bloko-tag-list"]//'
              'div[contains(@data-qa, "skills-element")]/'
              'span[@data-qa="bloko-tag__text"]/text()',
    "author": '//a[@data-qa="vacancy-company-name"]/@href',
}

HH_COMPANY_XPATH = {
    "title": '//div[@class="company-header"]//'
             'span[@data-qa="company-header-title-name"]/text()',
    "site": '//div[@class="employer-sidebar"]//'
            'a[@data-qa="sidebar-company-site"]/@href',
    "activities": '//div[@class="employer-sidebar-content"]//'
                  'div[@class="employer-sidebar-block"]/p/text()',
    "description": '//div[@data-qa="company-description-text"]//text()',
}

HH_COMPANY_VACANCY_XPATH = \
    '//div[@class="employer-sidebar"]//a[@data-qa="employer-page__employer-vacancies-link"]/@href'

