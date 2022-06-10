from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
import streamlit as st
import time


def train_window():

    st.header('Training parameters')
    training_parameters_section()
    st.markdown(f'---')
    
    if st.session_state['oracle'] == 'user':
        st.markdown(f"## Labeling: <font color='gray'>{st.session_state.task}", unsafe_allow_html=True)
        labeling_section()
        st.markdown(f'---')
    
    _, center, _ = st.columns([2,1,2])
    with center:
        retrain = st.button('Retrain Model')
    
    if retrain:
        progress_bar = st.progress(0)
        for i in range(1, st.session_state.n_models+1):
            st.session_state[f'model_{i}'].active_learning_procedure(n_queries=st.session_state['n_epochs'], 
                                                                     query_size=st.session_state['query_size'], 
                                                                     train_acc=True,
                                                                     progress_bar=progress_bar)
            
            print('$ train finished')
            #progress_bar.progress(int((i)/st.session_state.n_models*100))

        st.success('Model sucessfully retrained')
        



def training_parameters_section():
    #modify = st.checkbox('modify parameters')

    cols = st.columns([1,1,1,1,1,1,1])
    with cols[0]:
        st.markdown('Task')
        st.markdown(f"<font color='gray'>{st.session_state.task}", unsafe_allow_html=True)
    with cols[1]:
        st.markdown('Dataset')
        st.markdown(f"<font color='gray'>{st.session_state.dataset_data_path}", unsafe_allow_html=True)
#    if modify:
    with cols[2]:
        st.session_state['oracle'] = st.selectbox('Oracle', ['computer', 'user'])
    with cols[3]:
        st.session_state['query_size'] = st.slider('Query size', 1, 100, 10)
    with cols[4]:
        st.session_state['device'] = st.selectbox('Device', ['cpu', 'gpu'])
    
    if st.session_state['oracle'] == 'computer':
        with cols[5]:
            st.session_state['n_epochs'] = st.number_input('number of epochs', min_value=1, max_value=500, value=2, step=1)
""""               
    else:
        with cols[2]:
            st.markdown('Oracle')
            st.markdown(f"<font color='gray'>{st.session_state.oracle}", unsafe_allow_html=True)
        with cols[3]:
            st.markdown('Query size')
            st.markdown(f"<font color='gray'>{st.session_state.query_size}", unsafe_allow_html=True)
        with cols[4]:
            st.markdown('Device')
            st.markdown(f"<font color='gray'>{st.session_state.device}", unsafe_allow_html=True)
        
        if st.session_state['oracle'] == 'computer':
            with cols[5]:
                st.markdown('N epochs')
                st.markdown(f"<font color='gray'>{st.session_state.n_epochs}", unsafe_allow_html=True)    
"""        


def labeling_section():
    if st.session_state.task == 'classification':
        classification_task()
    elif st.session_state.task == 'object_detection':
        object_detection_task()


def classification_task():
        cols4 = st.columns([2,1,1,2])

        with cols4[0]:
            fig = plt.figure(figsize=(1,1))
            
            plt.imshow(st.session_state.dataset.X_train[0][0], cmap='gray')
            plt.axis('off')
            st.pyplot(fig)

        with cols4[1]: 
            st.markdown('#\n'*5)
            st.radio('label', st.session_state.labels)
            validate = st.button('validate')

        if validate: 
            st.success('Label sucessfully saved !')
        else:
            st.markdown('#')


def object_detection_task():
    st.sidebar.title('Labeling tools')
    left,center,right = st.columns([2,4,2])

    with left:
        transform = st.checkbox('transform', False)

        if transform:
            drawing_mode = 'transform'
            class_selected = None
        else:
            drawing_mode = st.selectbox('Drawing tool', ('rect', 'polygon', 'freedraw'))
            class_selected = st.radio('Class', ('class1','class2', 'class3'))

    if class_selected =='class1':
        fill_color = 'rgba(255, 0, 0, 0.3)'
    elif class_selected =='class2':
        fill_color = 'rgba(0, 255, 0, 0.3)'
    elif class_selected =='class3':
        fill_color = 'rgba(0, 0, 255, 0.3)'
    else: 
        fill_color=None

        
    with right:
        st.button('validate')

    with center:
        canvas_result = st_canvas(
            fill_color=fill_color,
            stroke_width=2,
            stroke_color='#000',
            background_image=st.session_state.image,
            update_streamlit=False,
            height=500,
            drawing_mode=drawing_mode,
            key="canvas",
        )