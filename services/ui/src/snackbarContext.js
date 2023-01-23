import React from 'react';

const SnackbarContext = React.createContext();

export const SnackbarProvider = SnackbarContext.Provider;
export const SnackbarConsumer = SnackbarContext.Consumer;

