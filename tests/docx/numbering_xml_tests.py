from nose.tools import istest, assert_equal

from mammoth.docx.xmlparser import element as xml_element
from mammoth.docx.numbering_xml import read_numbering_xml_element
from mammoth.docx.styles_xml import NumberingStyle, Styles


@istest
def find_level_returns_none_if_num_with_id_cannot_be_found():
    numbering = _read_numbering_xml_element(xml_element("w:numbering"))
    assert_equal(None, numbering.find_level("47", "0"))


_sample_numbering_xml = xml_element("w:numbering", {}, [
    xml_element("w:abstractNum", {"w:abstractNumId": "42"}, [
        xml_element("w:lvl", {"w:ilvl": "0"}, [
            xml_element("w:numFmt", {"w:val": "bullet"})
        ]),
        xml_element("w:lvl", {"w:ilvl": "1"}, [
            xml_element("w:numFmt", {"w:val": "decimal"})
        ])
    ]),
    xml_element("w:num", {"w:numId": "47"}, [
        xml_element("w:abstractNumId", {"w:val": "42"})
    ])
])


@istest
def level_includes_level_index():
    numbering = _read_numbering_xml_element(_sample_numbering_xml)
    assert_equal("0", numbering.find_level("47", "0").level_index)
    assert_equal("1", numbering.find_level("47", "1").level_index)


@istest
def list_is_not_ordered_if_formatted_as_bullet():
    numbering = _read_numbering_xml_element(_sample_numbering_xml)
    assert_equal(False, numbering.find_level("47", "0").is_ordered)

@istest
def list_is_ordered_if_formatted_as_decimal():
    numbering = _read_numbering_xml_element(_sample_numbering_xml)
    assert_equal(True, numbering.find_level("47", "1").is_ordered)


@istest
def find_level_returns_none_if_level_cannot_be_found():
    numbering = _read_numbering_xml_element(_sample_numbering_xml)
    assert_equal(None, numbering.find_level("47", "2"))


@istest
def when_abstract_num_has_num_style_link_then_style_is_used_to_find_num():
    numbering = _read_numbering_xml_element(
        xml_element("w:numbering", {}, [
            xml_element("w:abstractNum", {"w:abstractNumId": "100"}, [
                xml_element("w:lvl", {"w:ilvl": "0"}, [
                    xml_element("w:numFmt", {"w:val": "decimal"}),
                ]),
            ]),
            xml_element("w:abstractNum", {"w:abstractNumId": "101"}, [
                xml_element("w:numStyleLink", {"w:val": "List1"}),
            ]),
            xml_element("w:num", {"w:numId": "200"}, [
                xml_element("w:abstractNumId", {"w:val": "100"}),
            ]),
            xml_element("w:num", {"w:numId": "201"}, [
                xml_element("w:abstractNumId", {"w:val": "101"}),
            ])
        ]),
        styles=Styles.create(numbering_styles={"List1": NumberingStyle(num_id="200")}),
    )
    assert_equal(True, numbering.find_level("201", "0").is_ordered)


def _read_numbering_xml_element(element, styles=None):
    if styles is None:
        styles = Styles.EMPTY

    return read_numbering_xml_element(element, styles=styles)
