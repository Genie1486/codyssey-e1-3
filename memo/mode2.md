모드2 설계

Sevices 
    filters = {"size_5" : Filter(list[list[float]], list[list[float]])}

    Filter() 만들어야 할듯... 
        __init__ (size:int) 하면 3*3 자동 생성되게 
        __init__ (filter_a: list[list[float]] , filter_b:list[list[float]])

    하다보니 MacResult 도 속성 추가 해야할 듯 size, total_calculat_count (변수명 맘에 안듬) 
        이 화면 만들 때 필요... 아마도 size 별로 내림차순 해서 화면에 뿌려주지 않을까... 

            #---------------------------------------
            # [3] 성능 분석 (평균/10회)
            #---------------------------------------
            크기       평균 시간(ms)    연산 횟수
            -------------------------------------
            3×3            0.010           9
            5×5            0.031           25
            13×13      0.187           169
            25×25      0.682           625
        
    Pattern 
        name = "size_5_2"
        pattern = list[list[float]]
        expected = "X"




    # [1] 필터 로드 작업하 때 필요

    load_filters()
        filters_dict = repository.get_filters()  data.filters.items() 

        for size_n, filters in filters_dict: 

            # 정규화 여기서 하는게 낫나?..
            cross_filter = filters.get("cross") or filters.get("Cross") # 내가 예상한 동작 : 하나가 None 이면 덮어씀
            x_filter = filters.get("x")

            self.filters.size_n = Filter(cross_filter, x_filter)            


    load_patterns()
        pattern_dict = repository.get_patterns()
        # 여기까지 와서 고민은.. Quiz 때 했던 것 처럼 repository에서부터 Pattern, Filter에 담아놓을까도 고민되지만... service에 있는게 더 편한가 싶기도 하고
        
        _get_pattern_size()  "size_5_1" -> 5
        _validate_and_parse_patterns() 위에 함수랑 유사하긴 함... 여기까지 와서 드는 생각은 float검사를 꼭 해야할까?!.. 
            size check 5*5 행렬인지...
            float 체크

        # 정규화 여기서? 아니면 Pattern에서? 
        # Pattern에서 한다면... expected == "X" -> "x" 뭐 이런 식으로        
        self.patterns.append(Pattern(name, input, expected))


    - -- size_5_1 ---
    Cross 점수: 1.0
    X 점수: 5.0
    판정: X | expected: X | PASS
    Cross, X Enum으로 관리해야하려나?...
    Cross 점수, 판정: Cross, expected: Cross 여기 저기 많이 쓰임
    # 근데... Cross인지 X인지는 어떻게 구분?
    Filter에는 filter_a, filter_b로 관리했는데?

    [[str|MacResult]]는 성능분석이나 결과요약에서도 쓸 수 있을듯

    출력 위함
    analyze_all_patterns()
        return [[str|MacResult]]


    analyze_pattern(pattern:Pattern)
        _get_pattern_size()  "size_5_1" -> "size_5"
        find_filter(size_5) -> cross_filter, x_filter
        
        mac_result = calculate_result(cross_filter, x_filter, pattern.pattern)


        return pattern.name , MacResult()




Reposotry

    load_data()
        data = data.json 읽어옴
        self.data = data

    예외 발생 service에서 잡자... 
    service에서 잡아서 파일이 없거나 깨졌으면 기본데이터로 시도...

    load_default_data() 
        하드코딩?!..
        self.data = default_data


    get_filters()
        filters를 리스트 형태로 반환
    
    get_patterns()
        patterns를 리스트 형태로 반환


