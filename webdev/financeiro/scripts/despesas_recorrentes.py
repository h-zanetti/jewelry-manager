import pandas as pd
import datetime as dt
from itertools import chain
from django.db.models.query_utils import Q
from dateutil.relativedelta import relativedelta

from webdev.financeiro.models import Despesa


def get_expenses():

    # Date range

    today = dt.date.today()
    start_dt = today.replace(day=1) - relativedelta(months=6)
    end_dt = today.replace(day=1) + relativedelta(months=6)
    dt_range = [start_dt + relativedelta(months=n) for n in range(12)]


    # Despesas variaveis

    desp_var = Despesa.objects.filter(repetir='', data__gte=start_dt, data__lt=end_dt)
    du_df = pd.DataFrame(desp_var.values())
    du_df['data'] = du_df['data'].apply(lambda x: x.replace(day=1))
    du_df = du_df.groupby('data')[['valor']].sum()
    df = du_df.reindex(dt_range, fill_value=0).reset_index()
    df['data'] = pd.to_datetime(df['data'])
    df['month'] = df['data'].dt.month
    df['end_month'] = df['data'].dt.strftime('%Y-%m')


    # Despesas fixas - anuais

    desp_a = Despesa.objects.filter(repetir='a', data_de_encerramento__gte=start_dt)
    da_df = pd.DataFrame(desp_a.values())
    da_df['data'] = da_df['data'].apply(lambda x: x.replace(day=1))
    da_df['data'] = pd.to_datetime(da_df['data'])
    da_df['month'] = da_df['data'].dt.month
    da_df['data_de_encerramento'] = pd.to_datetime(da_df['data_de_encerramento'])
    da_df['end_month'] = da_df['data_de_encerramento'].dt.strftime('%Y-%m')


    # Despesas fixas - mensais

    desp_m = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__gte=start_dt), repetir='m'
    )
    dm_df = pd.DataFrame(desp_m.values())
    dm_df['data'] = dm_df['data'].apply(lambda x: x.replace(day=1))
    dm_df['data'] = pd.to_datetime(dm_df['data'])
    dm_df['month'] = dm_df['data'].dt.month
    dm_df['data_de_encerramento'] = dm_df['data_de_encerramento'].fillna(end_dt)
    dm_df['data_de_encerramento'] = pd.to_datetime(dm_df['data_de_encerramento'])
    dm_df['end_month'] = dm_df['data_de_encerramento'].dt.strftime('%Y-%m')


    # Merge tables

    data = df.to_dict()
    for i, r in df.iterrows():
        fixed_a = da_df.loc[
            (da_df['data']<=r.data)& \
            (da_df['month']==r.month)& \
            (da_df['end_month']>=r.end_month),
            'valor'].sum()

        fixed_m = dm_df.loc[
            (dm_df['data']<=r.data)& \
            (dm_df['end_month']>=r.end_month),
            'valor'].sum()

        data['valor'][i] += fixed_a + fixed_m

    plot_df = pd.DataFrame(data)


    # Get table data

    start_month = today.replace(day=1)
    next_month = start_month + relativedelta(months=1)
    desp_var = Despesa.objects.filter(repetir='', data__year=today.year, data__month=today.month)
    desp_m = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__gte=start_month),
        repetir='m', data__lt=next_month
    )
    desp_a = Despesa.objects.filter(
        Q(data_de_encerramento=None) | Q(data_de_encerramento__gte=start_month),
        repetir='a', data__month=today.month, data__year__lte=today.year
    )
    transactions = sorted(
        chain(desp_var, desp_m, desp_a),
        key=lambda instance: instance.data
    )

    return plot_df, transactions, dt_range
