import scrapy

class ShiyanlouCoursesSpider(scrapy.Spider):
    """ ���� scrapy ������Ҫдһ�� Spider �࣬�����Ҫ�̳� scrapy.Spider��.��������ж���Ҫ�������վ�����ӡ���δӷ��ص���ҳ��ȡ���ݵȵȡ�
    """

    # �����ʶ���ţ���scrapy��Ŀ�п��ܻ��ж�����棬name���ڱ�ʶÿ�����棬������ͬ
    name = 'shiyanlou-courses'

    def start_requests(self):
        """ ��Ҫ����һ���ɵ������󣬵�����Ԫ����`scrapy.Request`���󣬿ɵ������������һ���б���ߵ�����������scrapy ��֪������Щ��ҳ��Ҫ��ȡ�ˡ�`scrapy.Request`����һ��url������һ��callback������urlָ��Ҫ��ȡ����ҳ��callback��һ���ص��������ڴ����ص���ҳ��ͨ����һ����ȡ���ݵ�parse������
        """

        # �γ��б�ҳ��urlģ��
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        # ����Ҫ��ȡ��ҳ��
        urls = (url_tmpl.format(i) for i in range(1, 23))
        # ����һ�������������� Request �����������ǿɵ�������
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response): 
        # ����ÿ���γ̵� div.course-body
        for course in response.css('div.course-body'):
            # ʹ�� css �﷨��ÿ�� course ��ȡ����
            yield {
                # �γ�����
                'name': course.css('div.course-name::text').extract_first(),
                # �γ�����
                'description': course.css('div.course-desc::text').extract_first(),
                # �γ����ͣ�ʵ��¥�Ŀγ�����ѡ���Ա��ѵ��Ӫ���֣���ѿγ̲�û��������ʾ��Ҳ����˵û�� span.pull-right �����ǩ��û�������ǩ�ʹ�������ѿγ̣�ʹ��Ĭ��ֵ����ѡ����ɡ�
                'type': course.css('div.course-footer span.pull-right::text').extract_first(default='Free'),
                # ע�� // ǰ��� . ,û�е�ı�ʾ�����ĵ����е� div.course-body���� . �Ű�Ŷ�ǵ�ǰ��������� div.course-body
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d+)[^\d]*')
            }


