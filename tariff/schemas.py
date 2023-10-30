coe_tariff_schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "region": "coe",
            "code": "coe_tariff_c_2020_2021",
            "name": "tariff_c",
            "display_name": "City of Ekhuruleni, 1-JUL-20--30-JUN-21 Tariff_C",
            "tariff_map": [],
            "high_demand_months": [6, 7, 8],
            "currency": "rand",
            "country": "SA",
            "period_start": "2020-07-01",
            "period_end": "2021-06-30",
            "expires": "2021-06-30",
            "meta": {
                "description": "Small business only",
                "description_extra": "This tariff will suit low consumption micro business customers who are on prepayment or postpaid metering",
                "connections": ["SINGLE_PHASE_230_V", "MULTI_PHASE_400_OR_230_V"],
                "capacity_max": "11kV",
            },
            "charges": [
                {
                    "name": "fixed_charge",
                    "rate_billing_type": "per_month",
                    "types": {"230_400_V": 2273.82, "LESS_11KV_230_400_V": 3227.17},
                },
                {
                    "name": "demand_charge",
                    "rate_billing_type": "per_max_kva_per_month",
                    "types": {
                        "high_demand": {
                            "230_400_V": 168.48,
                            "LESS_11KV_230_400_V": 165.46,
                            "230_400_V_DIRECT": 162.44,
                        },
                        "low_demand": {
                            "230_400_V": 140.4,
                            "LESS_11KV_230_400_V": 137.91,
                            "230_400_V_DIRECT": 135.37,
                        },
                    },
                    "base_rate": {},
                },
                {
                    "name": "network_access_charge",
                    "rate_billing_type": "per_max_kva_per_year",
                    "types": {
                        "230_400_V": 48.85,
                        "LESS_11KV_230_400_V": 47.99,
                        "230_400_V_DIRECT": 47.12,
                    },
                    "base_rate": {
                        "rate_billing_type": "per_month",
                        "units": 25,
                        "unit_type": "kva",
                    },
                },
                {
                    "name": "energy_charge",
                    "rate_billing_type": "per_kwh",
                    "types": {
                        "high_demand": {
                            "230_400_V": {
                                "peak": 2.2518,
                                "off_peak": 2.2518,
                                "standard": 2.2518,
                            },
                            "230_400_V_DIRECT": {
                                "peak": 2.2098,
                                "off_peak": 2.2098,
                                "standard": 2.2098,
                            },
                            "LESS_11KV_230_400_V": {
                                "peak": 2.168,
                                "off_peak": 2.168,
                                "standard": 2.168,
                            },
                        },
                        "low_demand": {
                            "230_400_V": {
                                "peak": 1.3468,
                                "off_peak": 1.3468,
                                "standard": 1.3468,
                            },
                            "230_400_V_DIRECT": {
                                "peak": 1.3229,
                                "off_peak": 1.3229,
                                "standard": 1.3229,
                            },
                            "LESS_11KV_230_400_V": {
                                "peak": 1.2987,
                                "off_peak": 1.2987,
                                "standard": 1.2987,
                            },
                        },
                    },
                    "base_rate": {},
                },
            ],
        }
    ],
    "required": [
        "region",
        "code",
        "name",
        "display_name",
        "tariff_map",
        "high_demand_months",
        "currency",
        "country",
        "period_start",
        "period_end",
        "expires",
        "meta",
        "charges",
    ],
    "properties": {
        "region": {
            "$id": "#/properties/region",
            "type": "string",
            "title": "The region schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["coe"],
        },
        "code": {
            "$id": "#/properties/code",
            "type": "string",
            "title": "The code schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["coe_tariff_c_2020_2021"],
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["tariff_c"],
        },
        "display_name": {
            "$id": "#/properties/display_name",
            "type": "string",
            "title": "The display_name schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["City of Ekhuruleni, 1-JUL-20--30-JUN-21 Tariff_C"],
        },
        "tariff_map": {
            "$id": "#/properties/tariff_map",
            "type": "array",
            "title": "The tariff_map schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [[]],
            "additionalItems": True,
            "items": {"$id": "#/properties/tariff_map/items"},
        },
        "high_demand_months": {
            "$id": "#/properties/high_demand_months",
            "type": "array",
            "title": "The high_demand_months schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [[6, 7]],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/high_demand_months/items",
                "anyOf": [
                    {
                        "$id": "#/properties/high_demand_months/items/anyOf/0",
                        "type": "integer",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": 0,
                        "examples": [6, 7],
                    }
                ],
            },
        },
        "currency": {
            "$id": "#/properties/currency",
            "type": "string",
            "title": "The currency schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["rand"],
        },
        "country": {
            "$id": "#/properties/country",
            "type": "string",
            "title": "The country schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["SA"],
        },
        "period_start": {
            "$id": "#/properties/period_start",
            "type": "string",
            "title": "The period_start schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["2020-07-01"],
        },
        "period_end": {
            "$id": "#/properties/period_end",
            "type": "string",
            "title": "The period_end schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["2021-06-30"],
        },
        "expires": {
            "$id": "#/properties/expires",
            "type": "string",
            "title": "The expires schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": ["2021-06-30"],
        },
        "meta": {
            "$id": "#/properties/meta",
            "type": "object",
            "title": "The meta schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "description": "Small business only",
                    "description_extra": "This tariff will suit low consumption micro business customers who are on prepayment or postpaid metering",
                    "connections": ["SINGLE_PHASE_230_V", "MULTI_PHASE_400_OR_230_V"],
                    "capacity_max": "11kV",
                }
            ],
            "required": [
                "description",
                "description_extra",
                "connections",
                "capacity_max",
            ],
            "properties": {
                "description": {
                    "$id": "#/properties/meta/properties/description",
                    "type": "string",
                    "title": "The description schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": ["Small business only"],
                },
                "description_extra": {
                    "$id": "#/properties/meta/properties/description_extra",
                    "type": "string",
                    "title": "The description_extra schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": [
                        "This tariff will suit low consumption micro business customers who are on prepayment or postpaid metering"
                    ],
                },
                "connections": {
                    "$id": "#/properties/meta/properties/connections",
                    "type": "array",
                    "title": "The connections schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "examples": [["SINGLE_PHASE_230_V", "MULTI_PHASE_400_OR_230_V"]],
                    "additionalItems": True,
                    "items": {
                        "$id": "#/properties/meta/properties/connections/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/meta/properties/connections/items/anyOf/0",
                                "type": "string",
                                "title": "The first anyOf schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": [
                                    "SINGLE_PHASE_230_V",
                                    "MULTI_PHASE_400_OR_230_V",
                                ],
                            }
                        ],
                    },
                },
                "capacity_max": {
                    "$id": "#/properties/meta/properties/capacity_max",
                    "type": "string",
                    "title": "The capacity_max schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": "",
                    "examples": ["11kV"],
                },
            },
            "additionalProperties": True,
        },
        "charges": {
            "$id": "#/properties/charges",
            "type": "array",
            "title": "The charges schema",
            "description": "An explanation about the purpose of this instance.",
            "default": [],
            "examples": [
                [
                    {
                        "name": "fixed_charge",
                        "rate_billing_type": "per_month",
                        "types": {"230_400_V": 2273.82, "LESS_11KV_230_400_V": 3227.17},
                    },
                    {
                        "name": "demand_charge",
                        "rate_billing_type": "per_max_kva_per_month",
                        "types": {
                            "high_demand": {
                                "230_400_V": 168.48,
                                "LESS_11KV_230_400_V": 165.46,
                                "230_400_V_DIRECT": 162.44,
                            },
                            "low_demand": {
                                "230_400_V": 140.4,
                                "LESS_11KV_230_400_V": 137.91,
                                "230_400_V_DIRECT": 135.37,
                            },
                        },
                        "base_rate": {},
                    },
                ]
            ],
            "additionalItems": True,
            "items": {
                "$id": "#/properties/charges/items",
                "anyOf": [
                    {
                        "$id": "#/properties/charges/items/anyOf/0",
                        "type": "object",
                        "title": "The first anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "name": "fixed_charge",
                                "rate_billing_type": "per_month",
                                "types": {
                                    "230_400_V": 2273.82,
                                    "LESS_11KV_230_400_V": 3227.17,
                                },
                            }
                        ],
                        "required": ["name", "rate_billing_type", "types"],
                        "properties": {
                            "name": {
                                "$id": "#/properties/charges/items/anyOf/0/properties/name",
                                "type": "string",
                                "title": "The name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": ["fixed_charge"],
                            },
                            "rate_billing_type": {
                                "$id": "#/properties/charges/items/anyOf/0/properties/rate_billing_type",
                                "type": "string",
                                "title": "The rate_billing_type schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": ["per_month"],
                            },
                            "types": {
                                "$id": "#/properties/charges/items/anyOf/0/properties/types",
                                "type": "object",
                                "title": "The types schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "230_400_V": 2273.82,
                                        "LESS_11KV_230_400_V": 3227.17,
                                    }
                                ],
                                "required": ["230_400_V", "LESS_11KV_230_400_V"],
                                "properties": {
                                    "230_400_V": {
                                        "$id": "#/properties/charges/items/anyOf/0/properties/types/properties/230_400_V",
                                        "type": "number",
                                        "title": "The 230_400_V schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": 0.0,
                                        "examples": [2273.82],
                                    },
                                    "LESS_11KV_230_400_V": {
                                        "$id": "#/properties/charges/items/anyOf/0/properties/types/properties/LESS_11KV_230_400_V",
                                        "type": "number",
                                        "title": "The LESS_11KV_230_400_V schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": 0.0,
                                        "examples": [3227.17],
                                    },
                                },
                                "additionalProperties": True,
                            },
                        },
                        "additionalProperties": True,
                    },
                    {
                        "$id": "#/properties/charges/items/anyOf/1",
                        "type": "object",
                        "title": "The second anyOf schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": {},
                        "examples": [
                            {
                                "name": "demand_charge",
                                "rate_billing_type": "per_max_kva_per_month",
                                "types": {
                                    "high_demand": {
                                        "230_400_V": 168.48,
                                        "LESS_11KV_230_400_V": 165.46,
                                        "230_400_V_DIRECT": 162.44,
                                    },
                                    "low_demand": {
                                        "230_400_V": 140.4,
                                        "LESS_11KV_230_400_V": 137.91,
                                        "230_400_V_DIRECT": 135.37,
                                    },
                                },
                                "base_rate": {},
                            }
                        ],
                        "required": ["name", "rate_billing_type", "types", "base_rate"],
                        "properties": {
                            "name": {
                                "$id": "#/properties/charges/items/anyOf/1/properties/name",
                                "type": "string",
                                "title": "The name schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": ["demand_charge"],
                            },
                            "rate_billing_type": {
                                "$id": "#/properties/charges/items/anyOf/1/properties/rate_billing_type",
                                "type": "string",
                                "title": "The rate_billing_type schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": "",
                                "examples": ["per_max_kva_per_month"],
                            },
                            "types": {
                                "$id": "#/properties/charges/items/anyOf/1/properties/types",
                                "type": "object",
                                "title": "The types schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "high_demand": {
                                            "230_400_V": 168.48,
                                            "LESS_11KV_230_400_V": 165.46,
                                            "230_400_V_DIRECT": 162.44,
                                        },
                                        "low_demand": {
                                            "230_400_V": 140.4,
                                            "LESS_11KV_230_400_V": 137.91,
                                            "230_400_V_DIRECT": 135.37,
                                        },
                                    }
                                ],
                                "required": ["high_demand", "low_demand"],
                                "properties": {
                                    "high_demand": {
                                        "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/high_demand",
                                        "type": "object",
                                        "title": "The high_demand schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": {},
                                        "examples": [
                                            {
                                                "230_400_V": 168.48,
                                                "LESS_11KV_230_400_V": 165.46,
                                                "230_400_V_DIRECT": 162.44,
                                            }
                                        ],
                                        "required": [
                                            "230_400_V",
                                            "LESS_11KV_230_400_V",
                                            "230_400_V_DIRECT",
                                        ],
                                        "properties": {
                                            "230_400_V": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/high_demand/properties/230_400_V",
                                                "type": "number",
                                                "title": "The 230_400_V schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [168.48],
                                            },
                                            "LESS_11KV_230_400_V": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/high_demand/properties/LESS_11KV_230_400_V",
                                                "type": "number",
                                                "title": "The LESS_11KV_230_400_V schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [165.46],
                                            },
                                            "230_400_V_DIRECT": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/high_demand/properties/230_400_V_DIRECT",
                                                "type": "number",
                                                "title": "The 230_400_V_DIRECT schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [162.44],
                                            },
                                        },
                                        "additionalProperties": True,
                                    },
                                    "low_demand": {
                                        "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/low_demand",
                                        "type": "object",
                                        "title": "The low_demand schema",
                                        "description": "An explanation about the purpose of this instance.",
                                        "default": {},
                                        "examples": [
                                            {
                                                "230_400_V": 140.4,
                                                "LESS_11KV_230_400_V": 137.91,
                                                "230_400_V_DIRECT": 135.37,
                                            }
                                        ],
                                        "required": [
                                            "230_400_V",
                                            "LESS_11KV_230_400_V",
                                            "230_400_V_DIRECT",
                                        ],
                                        "properties": {
                                            "230_400_V": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/low_demand/properties/230_400_V",
                                                "type": "number",
                                                "title": "The 230_400_V schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [140.4],
                                            },
                                            "LESS_11KV_230_400_V": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/low_demand/properties/LESS_11KV_230_400_V",
                                                "type": "number",
                                                "title": "The LESS_11KV_230_400_V schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [137.91],
                                            },
                                            "230_400_V_DIRECT": {
                                                "$id": "#/properties/charges/items/anyOf/1/properties/types/properties/low_demand/properties/230_400_V_DIRECT",
                                                "type": "number",
                                                "title": "The 230_400_V_DIRECT schema",
                                                "description": "An explanation about the purpose of this instance.",
                                                "default": 0.0,
                                                "examples": [135.37],
                                            },
                                        },
                                        "additionalProperties": True,
                                    },
                                },
                                "additionalProperties": True,
                            },
                            "base_rate": {
                                "$id": "#/properties/charges/items/anyOf/1/properties/base_rate",
                                "type": "object",
                                "title": "The base_rate schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [{}],
                                "required": [],
                                "additionalProperties": True,
                            },
                        },
                        "additionalProperties": True,
                    },
                ],
            },
        },
    },
    "additionalProperties": True,
}
