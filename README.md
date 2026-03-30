# virtue_bright

## 文件结构

以下结构来自当前 Git 已跟踪文件，与 `.gitignore` 规则一致（被忽略的路径不会出现在此树中）。

```
virtue_bright/
├── .gitignore
├── .python-version
├── README.md
├── api
│   ├── __init__.py
│   └── yaoud_api
│       ├── __init__.py
│       ├── aes_tool.py
│       ├── auth.py
│       ├── bi
│       │   ├── __init__.py
│       │   └── report.py
│       ├── bpm
│       │   ├── __init__.py
│       │   └── wflow.py
│       ├── cdp
│       │   ├── __init__.py
│       │   ├── grade.py
│       │   ├── grade_type.py
│       │   ├── group.py
│       │   ├── member_register_config.py
│       │   ├── member_status_operate_record.py
│       │   ├── member_user.py
│       │   ├── points_rule.py
│       │   └── reserve_fund_rules.py
│       ├── cp
│       │   ├── __init__.py
│       │   ├── goods.py
│       │   ├── stockout.py
│       │   └── supplier_goods.py
│       ├── distribution
│       │   ├── __init__.py
│       │   ├── delivery_price.py
│       │   ├── distribution.py
│       │   ├── ds_goods.py
│       │   ├── goods.py
│       │   ├── material_allocate.py
│       │   └── second_delivery.py
│       ├── external
│       │   ├── __init__.py
│       │   ├── externalcontact.py
│       │   ├── group_chat.py
│       │   └── user.py
│       ├── finance
│       │   ├── __init__.py
│       │   ├── account_set_config.py
│       │   ├── audit_record.py
│       │   ├── document_operate_log.py
│       │   ├── payment_record.py
│       │   ├── report.py
│       │   ├── settlement.py
│       │   ├── settlement_account.py
│       │   ├── store_invoice.py
│       │   ├── store_refund_order.py
│       │   ├── store_settlement.py
│       │   ├── supplier_invoice.py
│       │   ├── supplier_invoice_register.py
│       │   └── supplier_reconciliation.py
│       ├── general_tools.py
│       ├── infra
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── bus_other.py
│       │   ├── custom_form.py
│       │   ├── dictionary.py
│       │   ├── employee.py
│       │   ├── enterprise.py
│       │   ├── external.py
│       │   ├── label_type.py
│       │   ├── login_account.py
│       │   ├── organ.py
│       │   ├── param_License.py
│       │   ├── region.py
│       │   ├── role.py
│       │   ├── shop_info.py
│       │   ├── stores.py
│       │   └── system.py
│       ├── inventory
│       │   ├── __init__.py
│       │   ├── goods.py
│       │   ├── in_out_bound_record.py
│       │   ├── inventory.py
│       │   ├── iv.py
│       │   ├── loss.py
│       │   ├── out_bound.py
│       │   └── warehouse.py
│       ├── member
│       │   ├── __init__.py
│       │   └── bs.py
│       ├── mia
│       │   ├── __init__.py
│       │   ├── dictionary.py
│       │   ├── mia_other.py
│       │   └── settlement_info.py
│       ├── oms
│       │   ├── __init__.py
│       │   ├── after_sale.py
│       │   ├── order.py
│       │   └── prescription_register.py
│       ├── payment
│       │   ├── __init__.py
│       │   └── payment.py
│       ├── pos
│       │   ├── __init__.py
│       │   └── work_record.py
│       ├── product
│       │   ├── __init__.py
│       │   ├── bs.py
│       │   └── yd.py
│       ├── shop_product
│       │   ├── __init__.py
│       │   ├── adjust_audit.py
│       │   ├── group_product.py
│       │   ├── price.py
│       │   ├── shop_config.py
│       │   └── shop_product.py
│       ├── supplier
│       │   ├── __init__.py
│       │   └── bs.py
│       └── 接口清单.md
├── application
│   └── __init__.py
├── configs
│   ├── __init__.py
│   ├── address.py
│   ├── server.py
│   └── yaoud.py
├── main.py
├── pyproject.toml
├── setup.py
├── utils
│   ├── __init__.py
│   ├── async_db_connection.py
│   └── logger_manager.py
└── uv.lock
```
